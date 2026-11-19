from pathlib import Path
import sys
import matplotlib.pyplot as plt
import pandas as pd
from prepare_data import load_prices
from factors import add_factors
from backtest import long_short_returns, summary

ROOT=Path(__file__).parent
DATA=ROOT/'data/raw/Stocks_Data.xlsx'
OUT=ROOT/'outputs'; OUT.mkdir(exist_ok=True)
if not DATA.exists():
    raise FileNotFoundError('Place the authorised Bloomberg export at data/raw/Stocks_Data.xlsx')
panel=add_factors(load_prices(DATA))
returns=pd.concat([long_short_returns(panel, s) for s in ['momentum_12_1_rank','reversal_1m_rank','turnover_3m_rank']], ignore_index=True)
summary(returns).to_csv(OUT/'factor_summary.csv', index=False)
returns.to_csv(OUT/'monthly_long_short_returns.csv', index=False)
for signal, x in returns.groupby('signal'):
    plt.plot(x['month'], (1+x['net_return']).cumprod(), label=signal)
plt.legend(); plt.title('Long-short factor portfolios, net of assumed costs'); plt.tight_layout()
plt.savefig(OUT/'cumulative_returns.png', dpi=180)
print(summary(returns).to_string(index=False))
