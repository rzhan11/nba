import pandas as pd


def zmr2(ytrue: pd.Series, ypred: pd.Series) -> float:
    return 1 - ((ytrue - ypred) ** 2).sum() / (ytrue ** 2).sum()
