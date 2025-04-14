import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.entity.config_entity import ModelPusherConfig
from src.pipline.stage_01_data_ingestion_pipe import DataIngestionPipe
from src.pipline.stage_02_data_val_pipe import DataValidationPipe
from src.pipline.stage_03_data_transformation import DataTransfromPipe
from src.pipline.stage_04_model_trainer_pipe import ModelTrainerPipe
from src.pipline.stage_05_model_Eval_pipe import ModelEvalPipe
from src.entity.artifact_entity import ModelEvaluationArtifact
from src.components.model_pusher import ModelPusher
from src.logger.custom_logging import logger
from src.exception.expection import CustomException



class ModelPusherPipe:
    def __init__(self,model_eval_artifact:ModelEvaluationArtifact):
        self.model_pusher_config = ModelPusherConfig
        self.model_eval_artifact=model_eval_artifact
        
    def main(self):
        try:

            model_pusher=ModelPusher (self.model_eval_artifact,self.model_pusher_config)
            model_pusher_artifact = model_pusher.initiate_model_pusher()
            return model_pusher_artifact
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
        model_trainer_obj=ModelTrainerPipe(data_transformation_artifact=data_transform_artifact)
        model_trainer_artifact=model_trainer_obj.main()
        model_eval_obj = ModelEvalPipe(data_ingestion_artifact,model_trainer_artifact)
        model_eval_artifact= model_eval_obj.main()
        obj=ModelPusherPipe(model_eval_artifact=model_eval_artifact)
        obj.main()

    except Exception as e:
        logger.exception(e)
        raise e