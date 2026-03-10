import pandas as pd


def lagged_ewma(df: pd.DataFrame, col: str, span: int, fill: float = None,
                prior_weight: int = None, prior_value: float = None,
                date_col: str = 'date') -> pd.Series:
    """
    Compute a lagged EWMA of an arbitrary column, sorted by date.

    For each row on date X, the prediction uses only rows from dates
    strictly before X. Multiple rows on the same date all receive the
    same prediction (the end-of-day EWMA from date X-1).

    fill:         value used when no prior date exists. Defaults to the column mean.
    prior_weight: number of synthetic observations prepended to warm up the EWMA.
    prior_value:  value of the synthetic observations. Defaults to fill.

    Returns a Series indexed like df.
    """
    fill_val = fill if fill is not None else df[col].mean()
    prior_val = prior_value if prior_value is not None else fill_val

    df_sorted = df.sort_values(date_col)

    if prior_weight is not None:
        series = pd.concat([pd.Series([prior_val] * prior_weight), df_sorted[col].reset_index(drop=True)], ignore_index=True)
    else:
        series = df_sorted[col].reset_index(drop=True)
        prior_weight = 0

    ewma_full = series.ewm(span=span, adjust=False).mean()
    ewma_actual = ewma_full.iloc[prior_weight:].values

    eod_ewma = (
        pd.Series(ewma_actual, index=df_sorted.index)
        .groupby(df_sorted[date_col])
        .last()
        .shift(1)
        .fillna(fill_val)
    )

    return df[date_col].map(eod_ewma).reindex(df.index)
