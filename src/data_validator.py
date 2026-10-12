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
        converted=pd.to_numeric(result[col],errors="coerce")
        invalid=result[col].notna() & converted.isna()
        count=int(invalid.sum())
        if count: logger.warning("Removed %d rows with invalid numeric values in %s",count,col)
        result=result.loc[~invalid].copy()
        result[col]=pd.to_numeric(result[col],errors="coerce")
    logger.debug("Validation: %d -> %d rows",len(df),len(result))
    return result
