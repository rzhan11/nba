import pandas as pd
import matplotlib.pyplot as plt


def vcv(df: pd.DataFrame, sort: str, pred: str, resps: list, weight=1.0, filter=None):
    """
    Plot cumulative weighted covariance between pred and each resp,
    sorted by sort.

    sort:   column to sort on (x-axis)
    pred:   predictor column
    resps:  list of responder columns
    weight: column name for weights, or a scalar (default 1.0)
    filter: boolean Series or pandas query expression to subset rows
    """
    if filter is not None:
        df = df.query(filter)

    df = df.sort_values(sort, ignore_index=True).copy()

    if sort == 'date':
        df[sort] = pd.to_datetime(df[sort]).dt.date

    w = df[weight] if isinstance(weight, str) else pd.Series(weight, index=df.index)

    pred_vals = df[pred] - df[pred].mean()
    cum_var = (w * pred_vals * pred_vals).cumsum()

    fig, ax = plt.subplots(figsize=(10, 3))

    total_var = cum_var.iloc[-1]
    for resp in resps:
        resp_vals = df[resp] - df[resp].mean()
        cum_cov = (w * pred_vals * resp_vals).cumsum()
        beta = cum_cov.iloc[-1] / total_var
        ax.plot(cum_var, cum_cov, label=f'{resp}  (β={beta:.4f})')

    # Place ~10 ticks at evenly spaced x positions, labeled with sort values
    tick_positions = [cum_var.iloc[int(i * (len(cum_var) - 1) / 10)] for i in range(11)]
    tick_labels    = [df[sort].iloc[int(i * (len(df) - 1) / 10)] for i in range(11)]
    ax.set_xticks(tick_positions)
    ax.set_xticklabels(tick_labels, rotation=45, ha='right')

    ax.axhline(0, color='black', linewidth=0.8, linestyle='--')
    ax.set_xlabel(sort)
    ax.set_ylabel(f'cumulative {pred} · resp · w')
    ax.set_title(f'vcv: pred={pred}, sorted by {sort}')
    ax.legend(loc='upper left', bbox_to_anchor=(1, 1))
    fig.tight_layout()

    return ax
