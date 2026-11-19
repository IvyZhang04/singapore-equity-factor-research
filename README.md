# Singapore Equity Factor Research

An NUS Quantitative Finance group project on the Singapore equity market. We construct and evaluate price/volume and reversal signals, with attention to total-return benchmarking, transaction costs and short-selling assumptions.

## My contribution

Co-developed data preparation, single-factor evaluation and robustness checks for price/volume and reversal factors with a teammate.

## Research workflow

1. Reshape authorised Bloomberg exports into a stock-month panel.
2. Construct 12-1 momentum, one-month reversal and trailing turnover signals.
3. Form equal-weighted long-short portfolios from monthly cross-sectional signal ranks.
4. Apply explicit transaction-cost assumptions and report gross and net results.

## Run

The raw Bloomberg exports are not versioned. With authorised access, place `Stocks_Data.xlsx` in `data/raw/` and run:

```bash
pip install -r requirements.txt
python run_pipeline.py
```

Results are written to `outputs/`. This repository documents coursework research, not an investment recommendation or a live trading strategy.

## Included results

`factor_summary.csv` and `cumulative_returns.png` are the public project run produced from the authorised research extract. The raw vendor exports remain excluded from version control; they cannot be redistributed through this repository.
