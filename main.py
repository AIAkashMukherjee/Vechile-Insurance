from src.logger.custom_logging import logger
from src.exception.expection import CustomException
from src.pipline.stage_01_data_ingestion_pipe import DataIngestionPipe
from src.pipline.stage_02_data_val_pipe import DataValidationPipe
from src.pipline.stage_03_data_transformation import DataTransfromPipe
from src.pipline.stage_04_model_trainer_pipe import ModelTrainerPipe
from src.entity.artifact_entity import DataIngestionArtifact
import sys
def run_stage(stage_name, pipeline_class,*args):
    try:
        logger.info(f">>>>>> stage {stage_name} started <<<<<<")
        pipeline = pipeline_class(*args)
        artifact=pipeline.main()
        logger.info(f">>>>>> stage {stage_name} completed <<<<<<\n\nx==========x")
        return artifact
    except Exception as e:
        logger.exception(e)
        raise CustomException(e,sys)
    
if __name__ == "__main__":
 
    # Stage 1: Data Ingestion
    data_ingestion_artifact = run_stage("Data Ingestion", DataIngestionPipe)

    # Stage 2: Data Validation
    data_validation_artifact = run_stage("Data Validation", DataValidationPipe, data_ingestion_artifact)

    # Stage 3: Data Transformation
    data_transformation_artifact = run_stage("Data Transformation", DataTransfromPipe, data_ingestion_artifact, data_validation_artifact)

    # Stage 4: Model Trainer
    model_trainer_pipe=run_stage("Model Trainer",ModelTrainerPipe,data_transformation_artifact)
 