import os
import sys

from pandas import DataFrame
from sklearn.model_selection import train_test_split

from src.entity.config_entity import DataIngestionConfig
from src.entity.artifact_entity import DataIngestionArtifact
from src.exception.expection import CustomException
from src.logger.custom_logging import logging
from src.data_access.vechile_data import Vechile_Data


class DataIngestion:
    def __init__(self,data_ingestion_config:DataIngestionConfig=DataIngestionConfig()):
        try:
            self.config=data_ingestion_config
        except Exception as e:
            raise CustomException(e,sys)

    def export_data_into_feature_store(self)->DataFrame:
        try:
            my_data=Vechile_Data()
            df=my_data.export_collection_as_dataframe(collection_name=self.config.collection_name)
            logging.info(f"Shape of dataframe: {df.shape}")
            feature_store_path=self.config.feature_store_file_path
            os.makedirs(os.path.dirname(feature_store_path),exist_ok=True)
            df.to_csv(feature_store_path,index=False,header=True)
            return df    
        except Exception as e:
            raise CustomException(e,sys)
    def split_data_train_test(self,dataframe:DataFrame):    
        try:
            train_set,test_set=train_test_split(dataframe,test_size=self.config.train_test_split_ratio,random_state=42)
            logging.info("Performed train test split on the dataframe")

            dir_path=os.path.dirname(self.config.training_file_path)
            os.makedirs(dir_path,exist_ok=True)
            train_set.to_csv(self.config.training_file_path,index=False,header=True)
            test_set.to_csv(self.config.testing_file_path,index=False,header=True)
            logging.info(f"Exported train and test file path.")
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_ingestion(self)->DataIngestionArtifact:
        try:

            df=self.export_data_into_feature_store()
            logging.info("Got the data from mongodb")

            df=self.split_data_train_test(df)
            logging.info("Perforemd train test split")

            data_ingestion_artifact=DataIngestionArtifact(trained_file_path=self.config.training_file_path,
                                                          test_file_path=self.config.testing_file_path)
            
            logging.info(f"Data ingestion artifact: {data_ingestion_artifact}")
            
            return data_ingestion_artifact
            
        except Exception as e:
            raise CustomException(e,sys)    