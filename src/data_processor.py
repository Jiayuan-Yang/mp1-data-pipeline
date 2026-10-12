import logging
import pandas as pd
logger=logging.getLogger(__name__)

def remove_duplicates(df):
    before=len(df)
    result=df.drop_duplicates().copy()
    logger.debug("remove_duplicates: %d -> %d rows",before,len(result))
    return result

def handle_missing(df,axis="rows"):
    if axis not in ("rows","columns"):
        logger.error("Unsupported missing-value axis: %s",axis)
        raise ValueError(f"Unsupported missing-value axis: {axis}")
    before=df.shape[0 if axis=="rows" else 1]
    result=df.dropna(axis=0 if axis=="rows" else 1).copy()
    after=result.shape[0 if axis=="rows" else 1]
    logger.debug("handle_missing (%s): removed %d",axis,before-after)
    return result

def remove_outliers(df,columns,method,threshold):
    if method not in ("iqr","zscore"):
        logger.error("Unsupported outlier method: %s",method)
        raise ValueError(f"Unsupported outlier method: {method}")
    result=df.copy()
    for col in columns:
        if col not in result.columns:
            logger.warning("Outlier column missing: %s",col)
            continue
        if not pd.api.types.is_numeric_dtype(result[col]):
            logger.warning("Outlier column is not numeric: %s",col)
            continue
        s=result[col]
        if method=="iqr":
            q1,q3=s.quantile([0.25,0.75]); iqr=q3-q1
            keep=s.between(q1-threshold*iqr,q3+threshold*iqr) | s.isna()
        else:
            std=s.std(ddof=0)
            keep=(abs((s-s.mean())/std)<=threshold) | s.isna() if std and pd.notna(std) else pd.Series(True,index=s.index)
        before=len(result)
        result=result.loc[keep].copy()
        logger.debug("%s: method=%s, threshold=%s, removed=%d",col,method,threshold,before-len(result))
    return result

def process_data(df,config):
    settings=config.get("processing",{})
    result=df.copy()
    if settings.get("remove_duplicates",False): result=remove_duplicates(result)
    missing=settings.get("missing",{})
    if missing.get("enabled",False): result=handle_missing(result,missing.get("axis","rows"))
    outliers=settings.get("outliers",{})
    if outliers.get("enabled",False):
        result=remove_outliers(result,outliers.get("columns",[]),outliers.get("method","iqr"),outliers.get("threshold",1.5))
    return result

def create_cleaning_report(df_before,df_after):
    return {"rows_before":len(df_before),"rows_after":len(df_after),
        "rows_removed":len(df_before)-len(df_after),
        "columns_before":len(df_before.columns),"columns_after":len(df_after.columns),
        "columns_removed":len(df_before.columns)-len(df_after.columns)}
