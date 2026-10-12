from pathlib import Path
import logging
import json
import pandas as pd
import yaml
logger=logging.getLogger(__name__)

def load_csv(filepath):
    data=pd.read_csv(filepath)
    logger.info("Loaded CSV file: %s (%d rows)",filepath,len(data))
    return data

def load_json(filepath):
    with open(filepath,encoding="utf-8") as f: data=json.load(f)
    logger.info("Loaded JSON file: %s",filepath)
    return data

def load_yaml(filepath):
    with open(filepath,encoding="utf-8") as f: data=yaml.safe_load(f)
    logger.info("Loaded YAML file: %s",filepath)
    return data

def load_data(filepath):
    path=Path(filepath)
    extension=path.suffix.lower()
    if extension==".csv": return load_csv(path)
    if extension==".json": return load_json(path)
    if extension in (".yaml",".yml"): return load_yaml(path)
    logger.error("Unsupported file format: %s",extension)
    raise ValueError(f"Unsupported file format: {extension}")
