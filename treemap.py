# sector_treemap.py
import pandas as pd
import numpy as np
import yfinance as yf
import plotly.express as px

def _end_today_plus1_utc():
    # agar hari ini ikut (untuk preset period)
    return pd.Timestamp.utcnow().normalize() + pd.Timedelta(days=1)

def _download_prices(tickers, start=None, end=None, period="6mo", include_today=False):
    """
    - Jika start & end diberikan (custom range): TIDAK ada fallback/auto-adjust.
      Hanya menambah +1 hari ke 'end' agar yfinance menyertakan hari end (konvensi yfinance).
    - Jika period digunakan (preset): gunakan end = today+1 (UTC) bila include_today=True.
    """
    if start is not None and end is not None:
        df = yf.download(
            tickers,
            start=pd.to_datetime(start),
            end=pd.to_datetime(end) + pd.Timedelta(days=1),  # hanya agar end terikut
            interval="1d",
            auto_adjust=True, group_by="ticker", progress=False
        )
    else:
        kw = dict(tickers=tickers, period=period, interval="1d",
                  auto_adjust=True, group_by="ticker", progress=False)
        if include_today:
            kw["end"] = _end_today_plus1_utc()
        df = yf.download(**kw)
    return df

def _close_from(pxdata, tickers):
    if isinstance(pxdata.columns, pd.MultiIndex):
        cols0 = pxdata.columns.get_level_values(0)
        have = [t for t in tickers if t in cols0]
        return pd.DataFrame({t: pxdata[t]["Close"] for t in have})
    else:
        # single ticker
        c = pxdata["Close"].to_frame()
        if len(tickers) == 1:
            c.columns = [tickers[0]]
        return c

def _perf_window(close_df: pd.DataFrame) -> pd.Series:
    """Perf (last/first - 1) di dalam window. 
       Bila <2 baris trading → raise ValueError('NOT_ENOUGH_TRADING_DAYS')."""
    c = close_df.ffill().dropna(how="all")
    if c.shape[0] < 2:
        raise ValueError("NOT_ENOUGH_TRADING_DAYS")
    perf = (c.iloc[-1] / c.iloc[0] - 1.0)
    perf.name = "Perf"
    return perf

def build_sector_treemap(tickers, start=None, end=None, period="6mo", include_today=False):
    # 1) Harga
    pxdata = _download_prices(tickers, start=start, end=end, period=period, include_today=include_today)

    # 2) Close & validasi trading days
    close = _close_from(pxdata, tickers)
    if close.shape[0] == 0:
        # Tidak ada baris sama sekali dalam rentang (kemungkinan weekend/libur)
        raise ValueError("NO_TRADING_DATA")

    # 3) Perf (jika kurang dari dua hari trading → error agar UI beri warning)
    perf = _perf_window(close)

    # 4) Sector & Market Cap
    rows = []
    for t in perf.index:  # gunakan hanya ticker yang punya close
        sec = "Unknown"; cap = np.nan
        try:
            info = yf.Ticker(t).info
            sec = info.get("sector", "Unknown") or "Unknown"
            cap = float(info.get("marketCap", np.nan))
        except Exception:
            pass
        rows.append({"Ticker": t, "Sector": sec, "MarketCap": cap})
    df_info = pd.DataFrame(rows)

    # 5) Gabung + fallback market cap
    df = df_info.merge(perf.to_frame(), left_on="Ticker", right_index=True, how="left")
    if df["MarketCap"].isna().all():
        df["MarketCap"] = 1.0
    else:
        df["MarketCap"] = df["MarketCap"].fillna(df["MarketCap"].median(skipna=True) or 1.0)

    # 6) Treemap
    fig = px.treemap(
        df,
        path=["Sector", "Ticker"],
        values="MarketCap",
        color="Perf",
        color_continuous_scale=[(0, "red"), (0.5, "black"), (1, "green")],
        color_continuous_midpoint=0,
    )
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0), title="Sector Treemap")
    return fig, df  # df: Ticker, Sector, MarketCap, Perf
