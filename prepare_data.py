"""Transform Bloomberg-style wide exports into a monthly stock panel."""
from pathlib import Path
import pandas as pd

def load_prices(path: str | Path) -> pd.DataFrame:
    book = pd.ExcelFile(path); pieces = []
    for sheet in book.sheet_names:
        raw = pd.read_excel(path, sheet_name=sheet).rename(columns=lambda c: "date" if c == pd.read_excel(path, sheet_name=sheet, nrows=0).columns[0] else c)
        price_cols = [c for c in raw.columns if isinstance(c, str) and "UNADJUSTED PRICE" in c]
        volume_cols = [c for c in raw.columns if isinstance(c, str) and "TURNOVER BY VOLUME" in c]
        for price_col in price_cols:
            name = price_col.split(" - ")[0]; volume_col = next((c for c in volume_cols if c.startswith(name + " - ")), None)
            x = raw[["date", price_col] + ([volume_col] if volume_col else [])].copy().rename(columns={price_col:"price",volume_col:"turnover"})
            x["ticker"] = name; pieces.append(x)
    panel = pd.concat(pieces, ignore_index=True)
    panel["date"] = pd.to_datetime(panel["date"], errors="coerce"); panel["price"] = pd.to_numeric(panel["price"], errors="coerce")
    panel["turnover"] = pd.to_numeric(panel.get("turnover"), errors="coerce")
    panel = panel.dropna(subset=["date","price"]).sort_values(["ticker","date"]); panel["month"] = panel["date"].dt.to_period("M")
    monthly = panel.groupby(["ticker","month"],as_index=False).agg(price=("price","last"),turnover=("turnover","mean"))
    monthly["return_1m"] = monthly.groupby("ticker")["price"].pct_change(); return monthly
