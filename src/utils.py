"""Utilities for the data processing pipeline."""
import logging
from pathlib import Path
import yaml

logger = logging.getLogger(__name__)


def load_config(filepath=None):
    """Load and validate YAML processing settings."""
    path = Path(filepath) if filepath is not None else Path(__file__).resolve().parent.parent / 'config' / 'config.yaml'
    if not path.is_file():
        raise FileNotFoundError(f'Configuration file not found: {path}')
    with path.open('r', encoding='utf-8') as handle:
        config = yaml.safe_load(handle)
    if not isinstance(config, dict) or not isinstance(config.get('processing'), dict):
        raise ValueError('Configuration must contain a processing mapping')
    logger.info('Configuration loaded: %s', path)
    return config
