import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')


list_of_files = [
   "src/__init__.py",
    "src/components/__init__.py",
    "src/components/data_ingestion.py",  
    "src/components/data_validation.py",
    "src/components/data_transformation.py",
    "src/components/model_trainer.py",
    "src/components/model_evaluation.py",
    "src/components/model_pusher.py",
    "src/configuration/__init__.py",
    "src/configuration/mongo_db_connection.py",
    "src/configuration/aws_connection.py",
    "src/cloud_storage/__init__.py",
    "src/cloud_storage/aws_storage.py",
    "src/data_access/__init__.py",
    "src/data_access/vechile_data.py",
    "src/constants/__init__.py",
    "src/entity/__init__.py",
    "src/entity/config_entity.py",
    "src/entity/artifact_entity.py",
    "src/entity/estimator.py",
    "src/entity/s3_estimator.py",
    "src/exception/__init__.py",
    'src/exception/expection.py',
    "src/logger/__init__.py",
    'src/logger/custom_logging.py',
    "src/pipline/__init__.py",
    "src/pipline/training_pipeline.py",
    "src/pipline/prediction_pipeline.py",
    "src/utils/__init__.py",
    "src/utils/main_utils.py",
    "app.py",
    "requirements.txt",
    "Dockerfile",
    ".dockerignore",
    "demo.py",
    "setup.py",
    "pyproject.toml",
    "config/model.yaml",
    "config/schema.yaml",
]



for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)


    # for folder 
    if filedir !="":
        os.makedirs(filedir, exist_ok=True)
        logging.info(f"Creating directory; {filedir} for the file: {filename}")


    # for files
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass
            logging.info(f"Creating empty file: {filepath}")


    else:
        logging.info(f"{filename} is already exists")