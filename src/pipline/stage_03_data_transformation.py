import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.entity.config_entity import DataTransformationConfig
from src.pipline.stage_01_data_ingestion_pipe import DataIngestionPipe
from src.pipline.stage_02_data_val_pipe import DataValidationPipe
from src.entity.artifact_entity import DataIngestionArtifact,DataValidationArtifact
from src.components.data_transformation import DataTransformation
from src.logger.custom_logging import logger
from src.exception.expection import CustomException



class DataTransfromPipe:
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact,data_validation_artifact: DataValidationArtifact):
        self.data_transform_config = DataTransformationConfig()
        self.data_ingestion_artifact=data_ingestion_artifact
        self.data_validation_artifact=data_validation_artifact

    def main(self):
        try:

            data_transform=DataTransformation(self.data_ingestion_artifact,self.data_transform_config,self.data_validation_artifact)
            data_transform_artifact = data_transform.initate_data_transformation()
            return data_transform_artifact
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == '__main__':
    try:

        ingestion_obj = DataIngestionPipe()  
        data_ingestion_artifact = ingestion_obj.main() 
        data_val_obj = DataValidationPipe(data_ingestion_artifact=data_ingestion_artifact)
        data_validation_artifact = data_val_obj.main()

        obj = DataTransfromPipe(data_ingestion_artifact=data_ingestion_artifact,data_validation_artifact=data_validation_artifact)
        obj.main()

    except Exception as e:
        logger.exception(e)
        raise e