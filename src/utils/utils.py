from pathlib import Path
from typing import Dict, Union
import yaml
import os
import shutil


def load_yaml(yaml_path: Union[str, Path]) -> Dict:
    """ Open and return yaml config file """
    yaml_path = str(Path(yaml_path).resolve())
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)
    file.close()
    return config or {}


def save_as_yaml(yaml_path: Union[str, Path], config: Dict) -> None:
    """ Save dict as yaml config file"""
    yaml_path = str(Path(yaml_path).resolve())
    with open(yaml_path, 'w') as file:
        yaml.dump(config, file)
    file.close()


def create_or_empty_folder(path: Union[str, Path]) -> None:
    """ Empty specified folder if exists, create the older otherwise """
    path = str(Path(path).resolve())
    if os.path.isdir(path):
        shutil.rmtree(path)
    os.makedirs(path)
