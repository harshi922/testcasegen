import gdown
import urllib.request as request
from llmRAGtestcasegen.logging import logger
from llmRAGtestcasegen.utils.common import get_size
from pathlib import Path
import os 
from llmRAGtestcasegen.entity import DataIngestionConfig

class DataIngestion:
    def __init__(self, config: DataIngestionConfig):
        self.config = config
    

    def download_file(self):
        if not os.path.exists(self.config.local_data_file):
            gdown.download(f'https://drive.google.com/uc?id={self.config.source_URL.split("/")[-2]}', self.config.local_data_file, quiet=False)
            logger.info(f"Downloading file{self.config.local_data_file}")
        else:
            print("self.config.source_URL", self.config.source_URL.split('view')[-1])
            logger.info(f"File already exists with size {get_size(Path(self.config.local_data_file))}")