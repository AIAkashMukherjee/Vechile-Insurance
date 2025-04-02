import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.entity.config_entity import DataValidationConfig
from src.pipline.stage_01_data_ingestion_pipe import DataIngestionPipe
from src.entity.artifact_entity import DataIngestionArtifact
from src.components.data_validation import DataValidation
from src.logger.custom_logging import logger
from src.exception.expection import CustomException


class DataValidationPipe:
    def __init__(self,data_ingestion_artifact: DataIngestionArtifact):
        self.data_val_config = DataValidationConfig()
        self.data_ingestion_artifact=data_ingestion_artifact

    def main(self):
        try:

            data_val=DataValidation(self.data_ingestion_artifact,self.data_val_config)
            data_val_artifact = data_val.initate_data_validation()
            return data_val_artifact
        except Exception as e:
            raise CustomException(e,sys)

if __name__ == '__main__':
    try:

        ingestion_obj = DataIngestionPipe()  
        data_ingestion_artifact = ingestion_obj.main()  
        obj = DataValidationPipe(data_ingestion_artifact=data_ingestion_artifact)
        obj.main()

    except Exception as e:
        logger.exception(e)
        raise e   