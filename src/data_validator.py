import logging
import pandas as pd
logger=logging.getLogger(__name__)

def validate_dataframe(df,required_columns,numeric_columns):
    result=df.copy()
    for col in required_columns:
        if col not in result.columns:
            logger.error("Missing required column: %s",col)
            raise ValueError(f"Missing required column: {col}")
    for col in numeric_columns:
        if col not in result.columns:
            logger.error("Missing numeric column: %s",col)
            raise ValueError(f"Missing numeric column: {col}")
        invalid_rows = []
        for i, value in result[col].items():
            if pd.notna(value):
                try:
                    float(value)
                except (ValueError, TypeError):
                    logger.warning("Invalid numeric value in %s at row %s", col, i)
                    invalid_rows.append(i)
        if invalid_rows:
            logger.warning("Removed %d rows with invalid numeric values in %s", len(invalid_rows), col)
            result = result.drop(index=invalid_rows).copy()
        result[col] = pd.to_numeric(result[col])
    logger.debug("Validation: %d -> %d rows; valid=%d, removed=%d",
                 len(df), len(result), len(result), len(df) - len(result))
    return result
