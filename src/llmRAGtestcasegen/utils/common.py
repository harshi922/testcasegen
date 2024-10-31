import os
from box.exceptions import BoxValueError
import yaml
from pathlib import Path
from llmRAGtestcasegen.logging import logger
import json 
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from typing import Any
import base64
import wget


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """
    Reads a yaml file and returns a ConfigBox object
    Args:
        path_to_yaml: Path to the yaml file
    Raises:
        ValueError: If the file is empty
        e: empty file
    Returns:
        ConfigBox: ConfigBox object
    """
    try:
        with open(path_to_yaml, 'r') as file:
            content = yaml.safe_load(file)
            logger.info(f"Reading yaml file from {path_to_yaml} loaded suucessfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("yaml file is empty")
    except Exception as e:
        raise e 



@ensure_annotations
def create_directories(path_to_directories: list, verbose = True):
    """
    creates list of directories
    Args:
        path_to_directories (list): List of ptahs of directories to be created
        ignore_log (bool, optional): ignore if multiple dirs are to be created. Defaults to False.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Directory created at {path}")

@ensure_annotations
def save_json(path: Path, data: dict): 
    """
    Save Json data
    Args:
        path (Path): Path to save the json file
        data (dict): Data to be saved in json file 
    """

    with open(path, 'w') as f:
        json.dump(data, f, indent=4)

    logger.info(f"Json file saved at {path}")

@ensure_annotations
def save_bin(data: Any, path: Path):
    """
    Save binary files

    Args:
        data (Any): Data to be saved
        path (Path): Path to save the binary file
    """
    joblib.dump(value = data, filename=path)
    logger.info(f"Binary file saved at {path}")

@ensure_annotations
def load_bin(path: Path) -> Any:
    """
    Load binary files

    Args:
        path (Path): Path to load the binary file
    Returns:
        Any: Data loaded from the binary file
    """
    data = joblib.load(path)
    logger.info(f"Binary file loaded from {path}")
    return data 

@ensure_annotations
def get_size(path: Path) -> str:
    """
    Get the size of the file in KB
    Args:
        path (Path): Path to the file
    Returns:
        str: Size of the file in KB
    """
    size = round(os.path.getsize(path)/1024)
    return f"~{size} KB"

def download_file(url: str, outpath: str):
    """
    Download file from the url
    Args:
        url (str): URL of the file
    """
    try:
        filename = wget.download(url,out=Path(outpath))
        print(f"\nDownloaded: {filename}")
    except Exception as e:
        print(f"An error occurred: {e}")
    logger.info(f"File downloaded from {url} and saved")