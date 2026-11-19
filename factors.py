import pandas as pd
def add_factors(panel: pd.DataFrame) -> pd.DataFrame:
    x=panel.sort_values(["ticker","month"]).copy(); g=x.groupby("ticker",group_keys=False)
    x["momentum_12_1"]=g["price"].transform(lambda s:s.shift(1).pct_change(11)); x["reversal_1m"]=-g["return_1m"].shift(1)
    x["turnover_3m"]=g["turnover"].transform(lambda s:s.shift(1).rolling(3).mean()); x["forward_return_1m"]=g["return_1m"].shift(-1)
    for c in ["momentum_12_1","reversal_1m","turnover_3m"]: x[c+"_rank"]=x.groupby("month")[c].rank(pct=True)
    return x
