import os
from box.exceptions import BoxValueError
import yaml
from diseaseClassfier import logger
import json
import joblib
from ensure import ensure_annotations
from box import ConfigBox
from pathlib import Path
from typing import Any
import base64

@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads a YAML file and returns its content in a ConfigBox.

    Args:
        path_to_yaml (str): Path to the YAML file.

    Raises:
        ValueError: If the YAML file is empty.
        e: Exception for an empty file.

    Returns:
        ConfigBox: An object of type ConfigBox containing the YAML content.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            logger.info(f"YAML file '{path_to_yaml}' loaded successfully")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError("YAML file is empty")
    except Exception as e:
        raise e

@ensure_annotations
def create_directories(directory_paths: list, verbose=True):
    """Create a list of directories.

    Args:
        directory_paths (list): List of paths for directories to be created.
        verbose (bool, optional): If True, log information about the created directories. Defaults to True.
    """
    for path in directory_paths:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Directory created at: {path}")

@ensure_annotations
def save_json(json_path: Path, json_data: dict):
    """Save JSON data to a file.

    Args:
        json_path (Path): Path to the JSON file.
        json_data (dict): Data to be saved in the JSON file.
    """
    with open(json_path, "w") as file:
        json.dump(json_data, file, indent=4)

    logger.info(f"JSON file saved at: {json_path}")

@ensure_annotations
def load_json(json_path: Path) -> ConfigBox:
    """Load JSON file data.

    Args:
        json_path (Path): Path to the JSON file.

    Returns:
        ConfigBox: Data as class attributes instead of a dictionary.
    """
    with open(json_path) as file:
        content = json.load(file)

    logger.info(f"JSON file loaded successfully from: {json_path}")
    return ConfigBox(content)

@ensure_annotations
def save_binary(binary_data: Any, binary_path: Path):
    """Save binary data to a file.

    Args:
        binary_data (Any): Data to be saved as binary.
        binary_path (Path): Path to the binary file.
    """
    joblib.dump(value=binary_data, filename=binary_path)
    logger.info(f"Binary file saved at: {binary_path}")


@ensure_annotations
def load_binary(binary_path: Path) -> Any:
    """Load binary data from a file.

    Args:
        binary_path (Path): Path to the binary file.

    Returns:
        Any: Object stored in the file.
    """
    data = joblib.load(binary_path)
    logger.info(f"Binary file loaded from: {binary_path}")
    return data

@ensure_annotations
def get_file_size(file_path: Path) -> str:
    """Get the size of a file in kilobytes.

    Args:
        file_path (Path): Path of the file.

    Returns:
        str: Size in kilobytes as a formatted string.
    """
    size_in_kb = round(os.path.getsize(file_path) / 1024)
    return f"~ {size_in_kb} KB"

@ensure_annotations
def decode_image_and_save(img_string, file_name):
    """Decode image from base64 string and save it to a file.

    Args:
        img_string (str): Base64-encoded image string.
        file_name (str): Name of the file to save the decoded image.
    """
    img_data = base64.b64decode(img_string)
    with open(file_name, 'wb') as file:
        file.write(img_data)
        
@ensure_annotations
def encode_image_to_base64(image_path):
    """Encode an image file into a Base64 string.

    Args:
        image_path (str): Path to the image file.

    Returns:
        str: Base64-encoded image string.
    """
    with open(image_path, "rb") as file:
        return base64.b64encode(file.read()).decode()
