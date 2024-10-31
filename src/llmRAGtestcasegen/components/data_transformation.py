from dotenv import load_dotenv
import pinecone
from llmRAGtestcasegen.logging import logger
import time
import torch
from tqdm import tqdm
import pandas as pd
from langchain.text_splitter import (
    RecursiveCharacterTextSplitter,
    Language,
)
import importlib.util
import os 
from pathlib import Path
from llmRAGtestcasegen.entity import DataTransformationConfig

load_dotenv()  # Ensure environment variables are loaded

open_ai_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")

class DataTransformation:
    def __init__(self, config: DataTransformationConfig):

        self.config = config
        self.java_splitter = RecursiveCharacterTextSplitter.from_language(
            language=Language.JAVA, chunk_size=500, chunk_overlap=150
        )
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        # here
        self.embedding_model = None
        self.download_and_import_unixcoder()

        # self.embedding_model = UniXcoder("microsoft/unixcoder-base")
        # self.embedding_model.to(self.device)

    def download_and_import_unixcoder(self):
            download_dir = Path(self.config.model_download_path) 
            url = self.config.model_url
            unixcoder_path = download_dir / "unixcoder.py"            
            if not unixcoder_path.exists():
                try:
                    import wget
                    filename = wget.download(url, out=str(download_dir))
                    print(f"\nDownloaded: {filename}")
                except Exception as e:
                    logger.error(f"An error occurred while downloading UniXcoder: {e}")
                    raise e
            # Dynamically import UniXcoder
            spec = importlib.util.spec_from_file_location("unixcoder", str(unixcoder_path))
            unixcoder_module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(unixcoder_module)
            self.embedding_model = unixcoder_module.UniXcoder("microsoft/unixcoder-base")
            self.embedding_model.to(self.device)

    def get_embeddings_codebert(self, code_corpus):
        embeddings = []
        for code in code_corpus:
            tokens_ids = self.embedding_model.tokenize([code], mode="<encoder-only>")
            source_ids = torch.tensor(tokens_ids).to(self.device)
            _, nl_embedding = self.embedding_model(source_ids)
            norm_nl_embedding = torch.nn.functional.normalize(nl_embedding, p=2, dim=1)
            norm_nl_embedding = norm_nl_embedding.detach().cpu().numpy()[0].tolist()
            embeddings.append(norm_nl_embedding)
        return embeddings

    def create_embeddings(self):
        pinecone.init(api_key=pinecone_api_key, environment='gcp-starter')
        index_name = 'd4jcodebertembeds'

        if index_name not in pinecone.list_indexes():
            pinecone.create_index(index_name, dimension=768, metric='cosine')
            # Wait for index to initialize
            while not pinecone.describe_index(index_name).status['ready']:
                time.sleep(1)
        index = pinecone.Index(index_name)
        logger.info(f"Index {index_name} created successfully with info: {index.describe_index_stats()}")

        # Load and preprocess data
        df = pd.read_csv(Path(self.config.data_path), usecols=['Class', 'Methods', 'Repository', 'TestCase'])
        df = df[df['Repository'].isin(['commons-jxpath', 'commons-csv'])].reset_index(drop=True)
        
        # Split each code file into chunks
        new_rows = []
        for _, x in df.iterrows():
            java_chunks = self.java_splitter.create_documents([x['Methods']])
            new_rows.extend({'Class': x['Class'], 'Methods': chunk.page_content, 'Repository': x['Repository']}
                            for chunk in java_chunks)
        
        new_df = pd.DataFrame(new_rows)
        logger.info(f"Dataframe shape: {new_df.shape}")

        # Process and upload in batches
        batch_size = 4
        for i in tqdm(range(0, len(new_df), batch_size)):
            batch = new_df.iloc[i:i + batch_size]
            ids = [str(j) for j in batch.index]
            texts = batch['Methods'].tolist()
            embeddings = self.get_embeddings_codebert(texts)

            metadata = [{'Class': row['Class'], 'Methods': row['Methods'], 'Repository': row['Repository']}
                        for _, row in batch.iterrows()]
            try:
                index.upsert(vectors=list(zip(ids, embeddings, metadata)))
            except Exception as e:
                logger.error(f"Error upserting batch {i}: {e}")
                continue

        logger.info(f"Uploading completed: {index.describe_index_stats()}")
