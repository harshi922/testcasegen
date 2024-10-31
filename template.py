# to create a folder structure for a new project
import os
from pathlib import Path
import logging

# create logger
logging.basicConfig(level=logging.INFO, format='[%(asctime)s] : %(message)s:')

# create a new project folder
project_name = "llmRAGtestcasegen"

list_of_files = [
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    f"src/{project_name}/logging/__init__.py",
    "dvc.yaml",
    "params.yaml",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb", 
    "templates/index.html",
    "config/config.yaml",
]

for file in list_of_files:
    # Path auto formats path for os used 
    path = Path(file)
    file_dir, file_name = os.path.split(path)

    # create a directory if it does not exist
    if file_dir != "":
        os.makedirs(file_dir, exist_ok=True)
        logging.info(f"Directory creating: {file_dir} for file: {file_name}")
    # create a file if it does not exist 
    if (not os.path.exists(path) or os.path.getsize(path) == 0):
        with open(path, "w") as f:
            pass
            logging.info(f"Empty File created: {file_name}")
    else:
        logging.info(f"File already exists: {file_name}")
