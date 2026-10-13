# DS3500 MP1 Data Pipeline

This project is a command-line data pipeline that loads a CSV dataset and a YAML configuration file. The main `pipeline.py` script coordinates each stage of the workflow and handles errors. The `src/data_loaders.py` module reads CSV, JSON, and YAML files. The `src/data_validator.py` module checks required columns and removes invalid numeric values. The `src/data_processor.py` module removes duplicate rows, handles missing values, removes outliers, and creates a cleaning report. The `src/data_output.py` module saves the cleaned data to a CSV file, and `src/utils.py` provides logging and file-path validation. The configuration in `config/config.yaml` controls validation and cleaning without changing the processing functions. Sample input files are provided in `fixtures/` for testing.

## Install

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
python pipeline.py --input fixtures/sample_data.csv --output output/clean.csv --config config/config.yaml --verbose
```

The pipeline writes `output/clean.csv`, prints a cleaning report, and logs the validation and cleaning steps. The `output/` folder is ignored by Git.

The sample contains 100 rows. Validation removes 2 invalid numeric rows,
leaving 98 rows. Cleaning then removes 2 duplicates, 2 rows with missing
values, and 2 outliers, producing 92 rows and 5 columns in `output/clean.csv`.
The cleaning report starts with the validated data, so it counts 6 removed
rows rather than 8.

Example output (timestamps omitted):

```text
INFO     __main__ — Validation complete: 100 -> 98 rows
INFO     __main__ — Processing complete: 98 -> 92 rows
INFO     __main__ — Saved cleaned data to output/clean.csv

Cleaning report:
{'rows_before': 98, 'rows_after': 92, 'rows_removed': 6, 'columns_before': 5, 'columns_after': 5, 'columns_removed': 0}
```

## Error-handling example

```bash
python pipeline.py --input missing.csv --output output/clean.csv --config config/config.yaml
```

This logs an error and exits with status code 1.
