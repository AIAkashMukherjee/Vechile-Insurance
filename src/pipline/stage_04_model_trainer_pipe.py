import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.entity.config_entity import ModelTrainerConfig
from src.pipline.stage_01_data_ingestion_pipe import DataIngestionPipe
from src.pipline.stage_02_data_val_pipe import DataValidationPipe
from src.pipline.stage_03_data_transformation import DataTransfromPipe
from src.entity.artifact_entity import DataTransformationArtifact
from src.components.model_trainer import ModelTrainer
from src.logger.custom_logging import logger
from src.exception.expection import CustomException



class ModelTrainerPipe:
    def __init__(self,data_transformation_artifact: DataTransformationArtifact):
        self.model_trainer_config = ModelTrainerConfig()
        self.data_transformation_artifact=data_transformation_artifact

    def main(self):
        try:

            model_trainer=ModelTrainer(self.data_transformation_artifact,self.model_trainer_config)
            model_trainer_artifact = model_trainer.initate_model_trainer()
            return model_trainer_artifact
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == '__main__':
    try:

        ingestion_obj = DataIngestionPipe()  
        data_ingestion_artifact = ingestion_obj.main() 
        data_val_obj = DataValidationPipe(data_ingestion_artifact=data_ingestion_artifact)
        data_val_artifact=data_val_obj.main()
        data_transform_obj=DataTransfromPipe(data_ingestion_artifact,data_val_artifact)
        data_transform_artifact= data_transform_obj.main()
        obj = ModelTrainerPipe(data_transform_artifact)
        obj.main()

    except Exception as e:
        logger.exception(e)
        raise e