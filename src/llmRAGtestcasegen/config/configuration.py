from llmRAGtestcasegen.constants import *
from llmRAGtestcasegen.utils.common import read_yaml, create_directories
from pathlib import Path
from llmRAGtestcasegen.entity import DataIngestionConfig
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