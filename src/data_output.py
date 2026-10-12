import logging
from pathlib import Path
logger=logging.getLogger(__name__)

def save_data(df,filepath):
    path=Path(filepath)
    path.parent.mkdir(parents=True,exist_ok=True)
    df.to_csv(path,index=False)
    logger.debug("Saved %d rows to %s",len(df),path)
    return path
