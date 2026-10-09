"""DS 3500 MP1: command-line data processing pipeline."""
import argparse
import logging
import sys
from pathlib import Path

import pandas as pd

from src.data_loaders import load_data
from src.data_processor import process_data, create_cleaning_report
from src.utils import load_config

logger = logging.getLogger(__name__)


def setup_logging(verbose=False):
    logging.basicConfig(level=logging.DEBUG if verbose else logging.INFO,
                        format='%(asctime)s %(levelname)-8s %(message)s',
                        datefmt='%H:%M:%S')


def parse_arguments():
    parser = argparse.ArgumentParser(description='Run the data processing pipeline.')
    parser.add_argument('--input', '-i', required=True, help='Input CSV, JSON or YAML file')
    parser.add_argument('--output', '-o', required=True, help='Output file')
    parser.add_argument('--format', choices=['csv', 'json'], default='csv')
    parser.add_argument('--verbose', '-v', action='store_true')
    return parser.parse_args()


def validate_input(filepath):
    if Path(filepath).is_file():
        logger.info('Input file validated: %s', filepath)
        return True
    logger.error('Input file not found: %s', filepath)
    return False


def as_dataframe(data):
    """Convert supported loader results to tabular data."""
    if isinstance(data, pd.DataFrame):
        return data
    if isinstance(data, list):
        return pd.DataFrame(data)
    if isinstance(data, dict):
        # The supplied sample JSON stores its records in the 'Data' field.
        if isinstance(data.get('Data'), list):
            return pd.DataFrame(data['Data'])
        return pd.DataFrame([data])
    raise ValueError('Input must contain a table, list of records, or JSON object')


def main():
    args = parse_arguments()
    setup_logging(args.verbose)
    logger.debug('Arguments parsed: input=%s, output=%s, format=%s',
                 args.input, args.output, args.format)
    if not validate_input(args.input):
        return 1
    try:
        df = as_dataframe(load_data(args.input))
        config = load_config()
        before = df.copy()
        cleaned = process_data(df, config)
        report = create_cleaning_report(before, cleaned)
        print(report)
        destination = Path(args.output)
        destination.parent.mkdir(parents=True, exist_ok=True)
        if args.format == 'json':
            cleaned.to_json(destination, orient='records', indent=2)
        else:
            cleaned.to_csv(destination, index=False)
        logger.info('Processing complete: %d -> %d rows', len(before), len(cleaned))
        logger.info('Saved cleaned data to %s', destination)
        return 0
    except (ValueError, KeyError, OSError, TypeError) as exc:
        logger.error('Pipeline failed: %s', exc)
        return 1


if __name__ == '__main__':
    sys.exit(main())
