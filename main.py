
from llmRAGtestcasegen.pipeline.stage01_data_ingestion import DataIngestionTrainingPipeline
from llmRAGtestcasegen.pipeline.stage02_data_transformation import DataTransformationPipeline
from llmRAGtestcasegen.logging import logger

try:
    STAGE_NAME = "Data Ingestion Stage"
    logger.info(f"Starting {STAGE_NAME}")
    obj = DataIngestionTrainingPipeline()
    obj.main()
    logger.info(f"Completed {STAGE_NAME}")
    STAGE_NAME = "Data Transformation Stage"
    logger.info(f"Starting {STAGE_NAME}")
    obj = DataTransformationPipeline()
    obj.main()
    logger.info(f"Completed {STAGE_NAME}")
    # STAGE_NAME = "Training Stage"
    # logger.info(f"Starting {STAGE_NAME}")
    # obj = TrainingPipeline()
    # obj.main()
    # logger.info(f"Completed {STAGE_NAME}")
    # STAGE_NAME = "Evaluation Stage"
    # logger.info(f"Starting {STAGE_NAME}")
    # obj = EvaluationPipeline()
    # obj.main()
    # logger.info(f"Completed {STAGE_NAME}")
except Exception as e:
    logger.exception(e)
    raise e
