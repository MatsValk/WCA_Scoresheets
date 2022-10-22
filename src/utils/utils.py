from pathlib import Path
from typing import Dict
import yaml


def load_yaml(yaml_path: str) -> Dict:
    """ Open and return yaml config file """
    yaml_path = str(Path(yaml_path).resolve())
    with open(yaml_path, 'r') as file:
        config = yaml.safe_load(file)
    file.close()
    return config or {}


def save_as_yaml(yaml_path: str, config: Dict) -> None:
    """ Save dict as yaml config file"""
    yaml_path = str(Path(yaml_path).resolve())
    with open(yaml_path, 'w') as file:
        yaml.dump(config, file)
    file.close()
