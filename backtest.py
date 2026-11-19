import pandas as pd
def long_short_returns(panel, signal, q=.3, cost_bps=20.):
    rows=[]
    for month,x in panel.groupby("month"):
        x=x.dropna(subset=[signal,"forward_return_1m"])
        if len(x)<8: continue
        lo,hi=x[signal].quantile(q),x[signal].quantile(1-q); gross=x.loc[x[signal]>=hi,"forward_return_1m"].mean()-x.loc[x[signal]<=lo,"forward_return_1m"].mean()
        rows.append({"month":month.to_timestamp(),"signal":signal,"gross_return":gross,"net_return":gross-2*cost_bps/10000})
    return pd.DataFrame(rows)
def summary(returns):
    rows=[]
    for signal,x in returns.groupby("signal"):
        r=x.net_return.dropna(); rows.append({"signal":signal,"months":len(r),"mean_monthly_return":r.mean(),"annualized_return":(1+r.mean())**12-1,"annualized_volatility":r.std(ddof=1)*12**.5,"annualized_sharpe":r.mean()/r.std(ddof=1)*12**.5})
    return pd.DataFrame(rows)
