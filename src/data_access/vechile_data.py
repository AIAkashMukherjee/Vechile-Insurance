import sys
import pandas as pd
import numpy as np
from typing import Optional

from src.configuration.mongo_db_connection import MongoDBConnection
from src.constants import DATABASE_NAME
from src.exception.expection import CustomException


class Vechile_Data:
    def __init__(self):
        try:
            self.client = MongoDBConnection(Databse_name=DATABASE_NAME)
        except Exception as e:
            raise CustomException(e, sys)

    def export_collection_as_dataframe(self, collection_name: str,Database_name: Optional[str] = None) -> pd.DataFrame:
        
        try:
            if Database_name is None:
                collection=self.client.database[collection_name] 
            else:
                collection=self.client[Database_name][collection_name]

            df = pd.DataFrame(list(collection.find()))
            print(f"Data fecthed with len: {len(df)}")
            df=df.drop(columns=['_id'], errors='ignore')
            # if "id" in df.columns.to_list():
            #     df = df.drop(columns=["id"], axis=1)
            df.replace({"na":np.nan},inplace=True)
            return df
        except Exception as e:
            raise CustomException(e, sys)        