import pandas as pd


def lagged_ewma(df: pd.DataFrame, col: str, span: int = 250, fill: float = None) -> pd.Series:
    """
    Compute a lagged EWMA of an arbitrary column, sorted by date.

    For each row on date X, the prediction uses only rows from dates
    strictly before X. Multiple rows on the same date all receive the
    same prediction (the end-of-day EWMA from date X-1).

    fill: value used when no prior date exists. Defaults to the column mean.

    Returns a Series indexed like df.
    """
    fill_val = fill if fill is not None else df[col].mean()
    df_sorted = df.sort_values('date')

    # Compute running EWMA across all rows, then take the last value per date
    eod_ewma = (
        df_sorted[col]
        .ewm(span=span, adjust=False)
        .mean()
        .groupby(df_sorted['date'])
        .last()
        .shift(1)  # shift by one date
        .fillna(fill_val)
    )

    # Map each row's date to the previous date's end-of-day EWMA
    return df['date'].map(eod_ewma).reindex(df.index)
