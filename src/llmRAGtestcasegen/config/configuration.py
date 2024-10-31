from llmRAGtestcasegen.constants import *
from llmRAGtestcasegen.utils.common import read_yaml, create_directories
from llmRAGtestcasegen.entity import DataIngestionConfig,DataTransformationConfig
from pathlib import Path
import os
import wget
class ConfigManager:
    def __init__(
            self, 
            config__filepath = CONFIG_FILE_PATH,
            params_filepath = PARAMS_FILE_PATH):
        self.config = read_yaml(config__filepath)
        self.params = read_yaml(params_filepath)

        create_directories([self.config.artifacts_root]) 
    
    def get_data_ingestion_config(self) -> DataIngestionConfig:
        config = self.config.data_ingestion
        create_directories([config.root_dir])
        return DataIngestionConfig(
            root_dir = config.root_dir,
            source_URL = config.source_URL,
            local_data_file = config.local_data_file,
            unzip_dir = config.unzip_dir
        )
    
    def get_data_transformation_config(self) -> DataTransformationConfig:
        config = self.config.data_transformation
        create_directories([config.root_dir])
        dataconfig =  DataTransformationConfig(
            root_dir = config.root_dir,
            data_path= config.data_path,
            embedding_model = config.embedding_model,
            model_url = config.model_url,
            model_download_path= config.model_download_path
        )
        # self.download_file(config.model_url,config.model_download_path)
        return dataconfig
