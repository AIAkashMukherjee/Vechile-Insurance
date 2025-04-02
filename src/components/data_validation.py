import json
import sys
import os
import pandas as pd
from pandas import DataFrame
from src.exception.expection import CustomException
from src.logger.custom_logging import logging
from src.utils.main_utils import read_yaml_file
from src.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from src.entity.config_entity import DataValidationConfig
from src.constants import SCHEMA_FILE_PATH


class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact, data_validation_config: DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
            
        except Exception as e:
            raise CustomException(e, sys)
        
    def validate_no_of_columns(self,df:DataFrame)->bool:
        try:
            status=len(df.columns)==len(self.schema_config['columns'])
            return status
        except Exception as e:
            raise CustomException(e, sys)    
        
    @staticmethod
    def read_data(file_path) -> DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as e:
            raise CustomException(e, sys)    

    def is_col_exists(self,df:DataFrame)->bool:
        try:
            df_columns = df.columns
            missing_numerical_columns=[]
            missing_cat_col=[]

            for col in self.schema_config['numerical_columns']:
                if col not in df_columns:
                    missing_numerical_columns.append(col)
                if len(missing_numerical_columns)>0:
                    logging.info(f"Missing numerical column: {missing_numerical_columns}")


            for column in self.schema_config["categorical_columns"]:
                if column not in df_columns:
                    missing_cat_col.append(column)

            if len(missing_cat_col)>0:
                logging.info(f"Missing categorical column: {missing_cat_col}")

            return False if len(missing_cat_col)>0 or len(missing_numerical_columns)>0 else True


        except Exception as e:
            raise CustomException(e, sys)
        
    def initate_data_validation(self)->DataValidationArtifact:
        try:
            validation_error_msg = ""
            train_df,test_df=(DataValidation.read_data(file_path=self.data_ingestion_artifact.trained_file_path),
                                 DataValidation.read_data(file_path=self.data_ingestion_artifact.test_file_path))
            
            status=self.validate_no_of_columns(train_df)
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe. "
            else:
                logging.info(f"All required columns present in training dataframe: {status}")

            status = self.validate_no_of_columns(test_df)
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe. "
            else:
                logging.info(f"All required columns present in testing dataframe: {status}")

            status = self.is_col_exists(train_df)
            if not status:
                validation_error_msg += f"Columns are missing in training dataframe. "
            else:
                logging.info(f"All categorical/int columns present in training dataframe: {status}")

            status = self.is_col_exists(test_df)
            if not status:
                validation_error_msg += f"Columns are missing in test dataframe."
            else:
                logging.info(f"All categorical/int columns present in testing dataframe: {status}")    

            validation_status=len(validation_error_msg)==0

            data_validation_artifact = DataValidationArtifact(
                validation_status=validation_status,
                message=validation_error_msg,
                validation_report_file_path=self.data_validation_config.validation_report_file_path
            )

            # Ensure the directory for validation_report_file_path exists
            report_dir = os.path.dirname(self.data_validation_config.validation_report_file_path)
            os.makedirs(report_dir, exist_ok=True)

            # Save validation status and message to a JSON file
            validation_report = {
                "validation_status": validation_status,
                "message": validation_error_msg.strip()
            }

            with open(self.data_validation_config.validation_report_file_path, "w") as report_file:
                json.dump(validation_report, report_file, indent=4)

            logging.info("Data validation artifact created and saved to JSON file.")
            logging.info(f"Data validation artifact: {data_validation_artifact}")
            return data_validation_artifact

        except Exception as e:
            raise CustomException(e, sys)    