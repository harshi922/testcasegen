from llmRAGtestcasegen.config.configuration import ConfigManager
from llmRAGtestcasegen.components.data_transformation import DataTransformation
from llmRAGtestcasegen.logging import logger

STAGE_NAME = "Data Transformation Stage"

class DataTransformationPipeline:
    def __init__(self):
        pass
    def main(self):
        config = ConfigManager()
        data_trans_config = config.get_data_transformation_config()
        data_transformer = DataTransformation(data_trans_config)
        data_transformer.create_embeddings()

if __name__ == "__main__":
    try:
        logger.info(f"Starting {STAGE_NAME}")
        obj = DataTransformationPipeline()
        obj.main()
        logger.info(f"Completed {STAGE_NAME}")
    except Exception as e:
        logger.exception(e)
        raise e
