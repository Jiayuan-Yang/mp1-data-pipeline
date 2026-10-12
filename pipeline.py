"""DS3500 MP1: configurable command-line data pipeline."""
import argparse
import logging
import sys
import pandas as pd
from src import (create_cleaning_report,load_data,process_data,save_data,
                 setup_logging,validate_dataframe,validate_input)
logger=logging.getLogger(__name__)

def parse_arguments():
    parser=argparse.ArgumentParser(description="Load, validate, clean, and save CSV data")
    parser.add_argument("--input","-i",required=True,help="Input CSV file")
    parser.add_argument("--config",required=True,help="YAML configuration file")
    parser.add_argument("--output","-o",required=True,help="Output CSV file")
    parser.add_argument("--verbose","-v",action="store_true",help="Enable DEBUG logging")
    return parser.parse_args()

def main():
    args=parse_arguments()
    setup_logging(args.verbose)
    logger.debug("Arguments parsed: input=%s, output=%s, config=%s",args.input,args.output,args.config)
    if not validate_input(args.input) or not validate_input(args.config): sys.exit(1)
    try:
        data=load_data(args.input)
        config=load_data(args.config)
        if not isinstance(data,pd.DataFrame): raise ValueError("Input data must be CSV tabular data")
        if not isinstance(config,dict): raise ValueError("Configuration must be a YAML mapping")
    except (ValueError,OSError,pd.errors.ParserError) as exc:
        logger.error("Loading failed: %s",exc)
        sys.exit(1)
    try:
        validation=config.get("validation",{})
        validated=validate_dataframe(data,validation.get("required_columns",[]),validation.get("numeric_columns",[]))
    except (ValueError,TypeError,KeyError) as exc:
        logger.error("Validation failed: %s",exc)
        sys.exit(1)
    logger.info("Validation complete: %d -> %d rows",len(data),len(validated))
    try:
        cleaned=process_data(validated,config)
    except (ValueError,TypeError,KeyError) as exc:
        logger.error("Processing failed: %s",exc)
        sys.exit(1)
    logger.info("Processing complete: %d -> %d rows",len(validated),len(cleaned))
    try:
        path=save_data(cleaned,args.output)
    except OSError as exc:
        logger.error("Saving failed: %s",exc)
        sys.exit(1)
    logger.info("Saved cleaned data to %s",path)
    print("\nCleaning report:")
    print(create_cleaning_report(validated,cleaned))

if __name__=="__main__":
    main()
