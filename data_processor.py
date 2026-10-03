import logging
import pandas as pd

logger = logging.getLogger(__name__)


def remove_duplicates(df):
    """Remove duplicate rows."""
    rows_before = len(df)
    result = df.drop_duplicates()
    rows_after = len(result)

    logger.debug(
        "remove_duplicates: %d → %d rows",
        rows_before,
        rows_after
    )

    return result


def handle_missing(df, axis="rows"):
    """Drop rows or columns containing missing values."""
    if axis == "rows":
        rows_before = len(df)
        result = df.dropna()
        rows_after = len(result)

        logger.debug(
            "handle_missing: %d → %d rows",
            rows_before,
            rows_after
        )

        return result

    elif axis == "columns":
        columns_before = len(df.columns)
        result = df.dropna(axis=1)
        columns_after = len(result.columns)

        logger.debug(
            "handle_missing: %d → %d columns",
            columns_before,
            columns_after
        )

        return result

    else:
        logger.error("Unsupported axis: %s", axis)
        raise ValueError(f"Unsupported axis: {axis}")


def remove_outliers(df, columns, method, threshold):
    """Remove outliers from the specified numeric columns."""
    if method not in ["iqr", "zscore"]:
        logger.error("Unsupported outlier method: %s", method)
        raise ValueError(f"Unsupported outlier method: {method}")

    result = df.copy()

    for column in columns:
        if column not in result.columns:
            logger.warning("Column not found: %s", column)
            continue

        if not pd.api.types.is_numeric_dtype(result[column]):
            logger.warning("Column is not numeric: %s", column)
            continue

        rows_before = len(result)

        if method == "iqr":
            q1 = result[column].quantile(0.25)
            q3 = result[column].quantile(0.75)
            iqr = q3 - q1

            lower = q1 - threshold * iqr
            upper = q3 + threshold * iqr

            result = result[
                (result[column] >= lower) &
                (result[column] <= upper)
            ]

            rows_removed = rows_before - len(result)

            logger.debug(
                "%s: lower=%s, upper=%s, removed=%d",
                column,
                lower,
                upper,
                rows_removed
            )

        elif method == "zscore":
            mean = result[column].mean()
            std = result[column].std()

            if std == 0 or pd.isna(std):
                rows_removed = 0
            else:
                z_scores = (result[column] - mean).abs() / std
                result = result[z_scores <= threshold]
                rows_removed = rows_before - len(result)

            logger.debug(
                "%s: method=%s, threshold=%s, removed=%d",
                column,
                method,
                threshold,
                rows_removed
            )

    return result


def process_data(df, config):
    """Apply the processing steps enabled in the configuration."""
    processing = config["processing"]

    result = df.copy()

    if processing.get("remove_duplicates", False):
        result = remove_duplicates(result)

    missing_config = processing.get("missing", {})
    if missing_config.get("enabled", False):
        result = handle_missing(
            result,
            axis=missing_config.get("axis", "rows")
        )

    outlier_config = processing.get("outliers", {})
    if outlier_config.get("enabled", False):
        result = remove_outliers(
            result,
            columns=outlier_config.get("columns", []),
            method=outlier_config.get("method"),
            threshold=outlier_config.get("threshold")
        )

    return result


def create_cleaning_report(df_before, df_after):
    """Return a dictionary summarizing the cleaning results."""
    return {
        "rows_before": len(df_before),
        "rows_after": len(df_after),
        "rows_removed": len(df_before) - len(df_after),
        "columns_before": len(df_before.columns),
        "columns_after": len(df_after.columns),
        "columns_removed": len(df_before.columns) - len(df_after.columns)
    }
