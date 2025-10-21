import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import numpy as np
import time
import datetime
import requests
import plotly.graph_objs as go


# --- Local Library Dictionaries ---
from i18n import tr, set_language
from currency import set_currency, get_currency, CURRENCIES, convert, currency_symbol
from analysis import aco_optimize_sharpe
from about import about_page
from homepage import homepage_content

languages = {'English': 'en', 'Bahasa Indonesia': 'id'}

# --- Persist language and currency in session state ---
if 'language' not in st.session_state:
    st.session_state['language'] = list(languages.keys())[0]
if 'currency' not in st.session_state:
    st.session_state['currency'] = list(CURRENCIES.keys())[0]
language = st.sidebar.selectbox(tr('Language'), list(languages.keys()), index=list(languages.keys()).index(st.session_state['language']), key='language')
currency = st.sidebar.selectbox(tr('Currency'), list(CURRENCIES.keys()), index=list(CURRENCIES.keys()).index(st.session_state['currency']), key='currency')

# --- Timezone selection ---
timezone_choices = {
    'Jakarta (UTC+7)': 'Asia/Jakarta',
    'New York (UTC-4/5)': 'America/New_York',
    'London (UTC+1/0)': 'Europe/London',
    'Zurich (UTC+2/1)': 'Europe/Zurich',
    'Tokyo (UTC+9)': 'Asia/Tokyo',
    'Shanghai (UTC+8)': 'Asia/Shanghai',
    'Hong Kong (UTC+8)': 'Asia/Hong_Kong',
    'Singapore (UTC+8)': 'Asia/Singapore',
    'Kolkata (UTC+5:30)': 'Asia/Kolkata',
    'Sydney (UTC+10)': 'Australia/Sydney',
    'UTC': 'UTC',
}
timezone_label = st.sidebar.selectbox('Chart Timezone', list(timezone_choices.keys()), index=list(timezone_choices.keys()).index('Jakarta (UTC+7)'))
selected_timezone = timezone_choices[timezone_label]
set_language(languages[st.session_state['language']])

# --- Navigation Bar ---
selected = option_menu(
    menu_title=None,
    options=[tr('Homepage'), tr('Stock Overview'), tr('Fundamental Overview'), tr('Syaria Stock Overview'), tr('Analysis'), tr('About Us')],
    icons=['house', 'bar-chart', 'table', 'check2-circle', 'graph-up', 'info-circle'],
    orientation='horizontal',
)

# --- Main Routing ---
if selected == tr('Homepage'):
    homepage_content()

elif selected == tr('Stock Overview'):
    st.header(tr('Stock Overview'))
    st.info(tr('Visualize stock prices and general info.'))
    # Compare checkbox
    compare_mode = st.checkbox(tr('Compare Stock'))
    # Ticker input
    if compare_mode:
        col1, col2 = st.columns([2, 2])
        with col1:
            ticker1 = st.text_input(tr('Stock Ticker 1'), value='AAPL', max_chars=10)
        with col2:
            ticker2 = st.text_input(tr('Stock Ticker 2'), value='', max_chars=10)
    else:
        ticker1 = st.text_input(tr('Stock Ticker'), value='AAPL', max_chars=10)
        ticker2 = ''
    chart_type = st.radio(tr('Chart Type'), ['Line', 'Candlestick'], horizontal=True)
    interval = st.selectbox(tr('Interval'), ['1m', '5m', '15m', '1h', '1d'])
    interval_valid_periods = {
        '1m': ['7d'],
        '5m': ['7d', '1mo'],
        '15m': ['7d', '1mo'],
        '1h': ['7d', '1mo'],
        '1d': ['1mo', '3mo', '6mo', '1y', '2y', '5y', 'max']
    }
    default_periods = ['1mo', '3mo', '6mo', '1y', '2y', '5y', 'max']
    valid_periods = interval_valid_periods.get(interval, default_periods)
    data_range = st.selectbox(tr('Range'), valid_periods)
    period_map = {p: p for p in valid_periods}
    indicator = st.selectbox(tr('Indicator'), ['None', 'Volume', 'SMA (Simple Moving Average)', 'EMA (Exponential Moving Average)', 'RSI (Relative Strength Index)'])
    use_custom_range = st.checkbox(tr('Use custom date range'))
    import datetime
    today = datetime.date.today()
    default_start = today - datetime.timedelta(days=30)
    start_date = st.date_input(tr('Start Date'), value=default_start, max_value=today) if use_custom_range else None
    end_date = st.date_input(tr('End Date'), value=today, min_value=default_start, max_value=today) if use_custom_range else None

    import yfinance as yf
    import pandas as pd
    tickers = [t for t in [ticker1, ticker2] if t]
    data_dict = {}
    info_dict = {}
    for t in tickers:
        try:
            if use_custom_range and start_date and end_date:
                start_dt = datetime.datetime.combine(start_date, datetime.time(0, 0))
                end_dt = datetime.datetime.combine(end_date, datetime.time(23, 59))
                data = yf.download(tickers=t, start=start_dt, end=end_dt, interval=interval)
            else:
                yf_period = period_map.get(data_range, '1mo')
                data = yf.download(tickers=t, period=yf_period, interval=interval)
            if data.empty:
                st.warning(f'No data found for {t} for this ticker/interval/range.')
                continue
            data.index = pd.to_datetime(data.index)
            if isinstance(data.columns, pd.MultiIndex):
                if all(col[0] in ['Open', 'High', 'Low', 'Close', 'Volume'] for col in data.columns):
                    data.columns = [col[0] for col in data.columns]
                else:
                    data.columns = ['_'.join([str(c) for c in col if c]) for col in data.columns]
            if 'Volume' in data.columns:
                data['Volume'] = pd.to_numeric(data['Volume'].astype(str).str.replace(',', ''), errors='coerce')
            data_dict[t] = data
            info_dict[t] = yf.Ticker(t).info
        except Exception as e:
            st.warning(f'Error fetching data for {t}: {e}')

    if data_dict:
        # Plot chart
        fig = go.Figure()
        import pytz
        # Use user-selected timezone for all charts
        for t, data in data_dict.items():
            if data.index.tz is None:
                data.index = data.index.tz_localize('UTC').tz_convert(selected_timezone)
            else:
                data.index = data.index.tz_convert(selected_timezone)
            if chart_type == 'Line':
                fig.add_trace(go.Scatter(x=data.index, y=data['Close'], mode='lines', name=f'{t} Close'))
            else:
                fig.add_trace(go.Candlestick(x=data.index,
                    open=data['Open'], high=data['High'], low=data['Low'], close=data['Close'], name=f'{t} Candlestick'))
            # Optionally add indicators for the first ticker only
            if t == ticker1:
                if indicator == 'Volume':
                    fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name=f'{t} Volume', yaxis='y2'))
                    fig.update_layout(yaxis2=dict(overlaying='y', side='right', title='Volume'))
                elif indicator == 'SMA (Simple Moving Average)':
                    sma = data['Close'].rolling(window=20).mean()
                    fig.add_trace(go.Scatter(x=data.index, y=sma, mode='lines', name=f'{t} SMA 20'))
                elif indicator == 'EMA (Exponential Moving Average)':
                    ema = data['Close'].ewm(span=20, adjust=False).mean()
                    fig.add_trace(go.Scatter(x=data.index, y=ema, mode='lines', name=f'{t} EMA 20'))
                elif indicator == 'RSI (Relative Strength Index)':
                    delta = data['Close'].diff()
                    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                    rs = gain / loss
                    rsi = 100 - (100 / (1 + rs))
                    fig.add_trace(go.Scatter(x=data.index, y=rsi, mode='lines', name=f'{t} RSI'))
        fig.update_layout(title='Stock Price Chart', xaxis_title='Date', yaxis_title='Price')
        st.plotly_chart(fig, use_container_width=True)

        # Show current price and general info for each ticker
        st.subheader(tr('Current Price and General Info'))
        cols = st.columns(len(tickers))
        selected_currency = get_currency()
        symbol = currency_symbol()
        for idx, t in enumerate(tickers):
            with cols[idx]:
                info = info_dict.get(t, {})
                price = data_dict[t]['Close'].iloc[-1] if not data_dict[t].empty else 'N/A'
                market_cap = info.get('marketCap', 'N/A')
                stock_currency = info.get('currency', 'USD')
                # Use the symbol for the stock's currency
                stock_symbol = CURRENCIES.get(stock_currency, {'symbol': stock_currency + ' '}).get('symbol', stock_currency + ' ')
                # Only convert if user's selected currency is different from the stock's
                if isinstance(price, (int, float)):
                    display_price = price
                    display_symbol = stock_symbol
                    if selected_currency != stock_currency:
                        try:
                            display_price = convert(price, stock_currency, selected_currency)
                            display_symbol = symbol
                        except Exception:
                            pass
                    st.metric(label=t, value=f"{display_symbol}{display_price:,.2f}")
                    price_str = f"{display_symbol}{display_price:,.2f}"
                else:
                    st.metric(label=t, value="-")
                    price_str = str(price)
                st.caption(info.get('shortName', ''))
                # Market Cap
                if isinstance(market_cap, (int, float)):
                    display_market_cap = market_cap
                    display_mc_symbol = stock_symbol
                    if selected_currency != stock_currency:
                        try:
                            display_market_cap = convert(market_cap, stock_currency, selected_currency)
                            display_mc_symbol = symbol
                        except Exception:
                            pass
                    market_cap_str = f"{display_mc_symbol}{display_market_cap:,.0f}"
                else:
                    market_cap_str = market_cap
                st.markdown(f'''
                    <div style="border:2px solid #2196f3; border-radius:12px; padding:1em; margin-bottom:1em; background:rgba(33,150,243,0.07); min-width:180px">
                        <div style='font-size:2em; font-weight:bold; color:#2196f3; margin-bottom:0.2em'>{price_str}</div>
                        <div style='font-size:1.1em; font-weight:600; margin-bottom:0.3em'>{info.get('shortName', t)}</div>
                        <div style='font-size:0.97em'><b>Sector:</b> {info.get('sector', 'N/A')}</div>
                        <div style='font-size:0.97em'><b>Industry:</b> {info.get('industry', 'N/A')}</div>
                        <div style='font-size:0.97em'><b>Exchange:</b> {info.get('exchange', 'N/A')}</div>
                        <div style='font-size:0.97em'><b>Currency:</b> {stock_currency}</div>
                        <div style='font-size:0.97em'><b>Market Cap:</b> {market_cap_str}</div>
                    </div>
                ''', unsafe_allow_html=True)

        # Show description for ticker1
        if ticker1 in info_dict:
            st.subheader(tr('Company Description'))
            desc = info_dict[ticker1].get('longBusinessSummary', info_dict[ticker1].get('shortName', 'No description available.'))
            st.write(desc)

elif selected == tr('Fundamental Overview'):
    st.header(tr('Fundamental Overview'))
    st.info(tr('View all available fundamental metrics for a stock.'))
    ticker = st.text_input(tr('Stock Ticker for Fundamentals'), value='AAPL', max_chars=10)
    if ticker:
        import yfinance as yf
        try:
            info = yf.Ticker(ticker).info
            fundamentals = {
                'Market Cap': info.get('marketCap'),
                'IPO': info.get('ipoExpectedDate', info.get('ipoDate', 'N/A')),
                'Exchange': info.get('exchange'),
                'Currency': info.get('currency'),
                'Sector': info.get('sector'),
                'Country': info.get('country'),
                'Industry': info.get('industry'),
                'Website': info.get('website'),
                'Employees': info.get('fullTimeEmployees'),
                'Trailing P/E': info.get('trailingPE'),
                'Forward P/E': info.get('forwardPE'),
                'PEG Ratio': info.get('pegRatio'),
                'EPS (TTM)': info.get('trailingEps'),
                'EPS (Forward)': info.get('forwardEps'),
                'Dividend Yield': info.get('dividendYield'),
                'Dividend Rate': info.get('dividendRate'),
                'Payout Ratio': info.get('payoutRatio'),
                'Book Value': info.get('bookValue'),
                'Price/Book': info.get('priceToBook'),
                'Profit Margin': info.get('profitMargins'),
                'Operating Margin': info.get('operatingMargins'),
                'Gross Margin': info.get('grossMargins'),
                'Return on Equity': info.get('returnOnEquity'),
                'Return on Assets': info.get('returnOnAssets'),
                'EBITDA': info.get('ebitda'),
                'Revenue (TTM)': info.get('totalRevenue'),
                'Revenue/Share': info.get('revenuePerShare'),
                'Quarterly Revenue Growth': info.get('revenueQuarterlyGrowth'),
                'Quarterly Earnings Growth': info.get('earningsQuarterlyGrowth'),
                'Debt/Equity': info.get('debtToEquity'),
                'Current Ratio': info.get('currentRatio'),
                'Quick Ratio': info.get('quickRatio'),
                'Beta': info.get('beta'),
                'Shares Outstanding': info.get('sharesOutstanding'),
                'Float Shares': info.get('floatShares'),
                'Held by Insiders': info.get('heldPercentInsiders'),
                'Held by Institutions': info.get('heldPercentInstitutions'),
                'Short Ratio': info.get('shortRatio'),
                'Short % of Shares Outstanding': info.get('shortPercentOfSharesOutstanding'),
                'Short % of Float': info.get('sharesShortPreviousMonthDate'),
            }
            import pandas as pd
            # Try to extract Interest Income and Interest Income Ratio
            interest_income_val = None
            total_revenue_val = None
            interest_income_ratio_str = "N/A"
            try:
                income_stmt = yf.Ticker(ticker).get_income_stmt()
                if isinstance(income_stmt, pd.DataFrame):
                    for key in ['Interest Income', 'InterestIncome', 'Total Interest Income']:
                        if key in income_stmt.index:
                            interest_income_val = income_stmt.loc[key].iloc[0]
                            break
                    for key in ['Total Revenue', 'TotalRevenue', 'Revenue']:
                        if key in income_stmt.index:
                            total_revenue_val = income_stmt.loc[key].iloc[0]
                            break
                if interest_income_val is not None and total_revenue_val is not None and total_revenue_val != 0:
                    interest_income_ratio = interest_income_val / total_revenue_val
                    interest_income_ratio_str = f"{interest_income_ratio:.2%}"
            except Exception:
                pass
            fundamentals['Interest Income'] = interest_income_val if interest_income_val is not None else 'N/A'
            fundamentals['Interest Income Ratio'] = interest_income_ratio_str

            # Convert all monetary values to selected currency
            selected_currency = get_currency()
            symbol = currency_symbol()
            monetary_keys = [
                'Market Cap', 'Book Value', 'EBITDA', 'Revenue (TTM)', 'Revenue/Share', 'Dividend Rate', 'Price/Book',
                'EPS (TTM)', 'EPS (Forward)', 'Total Assets', 'Total Debt', 'Interest Income'
            ]
            for key in monetary_keys:
                if key in fundamentals and isinstance(fundamentals[key], (int, float)):
                    fundamentals[key] = f"{symbol}{convert(fundamentals[key], 'USD', selected_currency):,.2f}"

            df = pd.DataFrame(list(fundamentals.items()), columns=['Metric', 'Value'])
            # Hide index and style table
            st.markdown('''
                <style>
                .styled-metric-table {
                    border-collapse: separate;
                    border-spacing: 0;
                    width: 100%;
                    font-size: 1.07em;
                    background: rgba(33,150,243,0.03);
                    border-radius: 12px;
                    overflow: hidden;
                }
                .styled-metric-table th {
                    background: #2196f3;
                    color: #fff;
                    font-weight: 600;
                    padding: 0.5em 0.8em;
                }
                .styled-metric-table td {
                    padding: 0.5em 0.8em;
                    border-bottom: 1px solid #e0e0e0;
                }
                .styled-metric-table tr:last-child td {
                    border-bottom: none;
                }
                </style>
            ''', unsafe_allow_html=True)
            st.markdown(df.to_html(index=False, classes='styled-metric-table'), unsafe_allow_html=True)

        except Exception as e:
            st.warning(f'Could not retrieve fundamentals: {e}')

elif selected == tr('Syaria Stock Overview'):
    st.header(tr('Syaria Stock Overview'))
    st.info(tr('Check if a stock is Sharia (Syariah) compliant based on OJK/HISSA-like (HISSA) criteria, using Yahoo Finance data.'))

    syaria_ticker = st.text_input(tr('Stock Ticker for Syaria Analysis'), value='AAPL', max_chars=10)
    import yfinance as yf
    import pandas as pd
    if syaria_ticker:
        try:
            info = yf.Ticker(syaria_ticker).info
            # Validate info
            if not info or not info.get('sector') or not info.get('shortName'):
                st.warning('Could not retrieve company data for this ticker. Please check the ticker symbol.')
            else:
                # HISSAA/OJK Shariah Criteria (ENGLISH):
                # 1. Company does NOT operate in forbidden business activities (see below)
                # 2. Total interest-based debt to total assets ≤ 45% (use Debt/Equity as proxy if assets not available)
                # 3. Total interest income and other non-halal income to total revenue + other income ≤ 10% (not available from yfinance)

                forbidden_sectors = [
                'Bank', 'Insurance', 'Tobacco', 'Alcohol', 'Gambling', 'Casino', 'Porn', 'Weapon', 'Aerospace', 'Defense',
                'Conventional', 'Financial', 'Lending', 'Loan', 'Beverages—Wineries & Distilleries', 'Adult', 'Lottery',
                'Pharmaceutical', 'Biotechnology', 'Brewery', 'Distillery', 'Mortgage', 'Pawn', 'Credit', 'Leasing', 'Brokerage',
                'Money', 'Securities', 'Investment', 'Riba', 'Interest', 'Shariah Non-Compliant'
            ]
            sector = info.get('sector', '')
            industry = info.get('industry', '')
            # Whitelist for known sharia-compliant tickers
            sharia_bank_tickers = ['BRIS.JK', 'BTPS.JK', 'PNBS.JK', 'BMSY.JK']  # Add more as needed
            non_sharia_blacklist = ['BBCA.JK']  # Always non-sharia, even if description contains 'sharia'
            company_name = info.get('shortName', '')
            description = info.get('longBusinessSummary', '')
            # Blacklist takes precedence
            if syaria_ticker.upper() in non_sharia_blacklist:
                sector_flag = False
            # If ticker is in whitelist or name/desc contains 'sharia' or 'syariah', override forbidden
            elif (syaria_ticker.upper() in sharia_bank_tickers or
                'sharia' in company_name.lower() or 'syariah' in company_name.lower() or
                'sharia' in description.lower() or 'syariah' in description.lower()):
                sector_flag = True
            else:
                forbidden_flag = any(s.lower() in (sector.lower() + ' ' + industry.lower()) for s in forbidden_sectors)
                sector_flag = not forbidden_flag

            # Debt/Equity (proxy for Debt/Assets)
            debt_to_equity = info.get('debtToEquity', None)
            debt_flag = (debt_to_equity is not None and debt_to_equity < 45)

            # Try to extract Interest Income and Revenue from yfinance income statement
            interest_income_val = None
            total_revenue_val = None
            try:
                income_stmt = yf.Ticker(syaria_ticker).get_income_stmt()
                if isinstance(income_stmt, pd.DataFrame):
                    # Try common variants for interest income
                    for key in ['Interest Income', 'InterestIncome', 'Total Interest Income']:
                        if key in income_stmt.index:
                            interest_income_val = income_stmt.loc[key].iloc[0]
                            break
                    # Try common variants for total revenue
                    for key in ['Total Revenue', 'TotalRevenue', 'Revenue']:
                        if key in income_stmt.index:
                            total_revenue_val = income_stmt.loc[key].iloc[0]
                            break
            except Exception:
                pass
            if interest_income_val is not None and total_revenue_val is not None and total_revenue_val != 0:
                interest_income_ratio = interest_income_val / total_revenue_val
                interest_income_str = f"{interest_income_ratio:.2%}"  # percentage
                interest_income_flag = interest_income_ratio < 0.10
            else:
                interest_income_str = "N/A"
                interest_income_flag = None

            # Compose results
            criteria = [
                {"Criterion": tr("No forbidden business activities (gambling, alcohol, tobacco, conventional finance, etc.)"),
                 "Value": f"{tr(sector)} / {tr(industry)}", "Pass": sector_flag},
                {"Criterion": tr("Interest-based Debt/Equity < 45% (proxy for Debt/Assets)"),
                 "Value": f"{debt_to_equity if debt_to_equity is not None else tr('N/A')}", "Pass": debt_flag if debt_to_equity is not None else None},
                {"Criterion": tr("Interest & other non-halal income / revenue < 10%"),
                 "Value": interest_income_str if interest_income_str != 'N/A' else tr('N/A'), "Pass": interest_income_flag},
            ]
            # Overall Shariah status
            passed = all(c['Pass'] is not False for c in criteria)
            st.markdown(f"""
                <div style='padding:1em; border-radius:10px; background:{'#e8f5e9' if passed else '#ffebee'}; border:2px solid {'#43a047' if passed else '#e53935'}; margin-bottom:1em;'>
                    <span style='font-size:1.4em; font-weight:bold; color:{'#43a047' if passed else '#e53935'}'>
                        {tr('✅ SHARIA COMPLIANT') if passed else tr('❌ NOT SHARIA COMPLIANT')}
                    </span><br>
                    <span style='font-size:1.1em; color:#222'>
                        {syaria_ticker.upper()} {info.get('shortName', '')}
                    </span>
                </div>
            """, unsafe_allow_html=True)
            # Styled table for criteria
            df = pd.DataFrame(criteria)
            st.markdown('''
                <style>
                .syaria-table {
                    border-collapse: separate;
                    border-spacing: 0;
                    width: 100%;
                    font-size: 1.07em;
                    background: rgba(33,150,243,0.03);
                    border-radius: 12px;
                    overflow: hidden;
                }
                .syaria-table th {
                    background: #2196f3;
                    color: #fff;
                    font-weight: 600;
                    padding: 0.5em 0.8em;
                }
                .syaria-table td {
                    padding: 0.5em 0.8em;
                    border-bottom: 1px solid #e0e0e0;
                }
                .syaria-table tr:last-child td {
                    border-bottom: none;
                }
                </style>
            ''', unsafe_allow_html=True)
            # Add Pass/Fail icons
            def pass_icon(val):
                if val is True:
                    return '✅'
                elif val is False:
                    return '❌'
                else:
                    return '—'
            df['Result'] = df['Pass'].apply(pass_icon)
            st.markdown(df[['Criterion', 'Value', 'Result']].to_html(index=False, classes='syaria-table'), unsafe_allow_html=True)
        except Exception as e:
            st.warning(f'Could not retrieve or analyze: {e}')

elif selected == tr('Analysis'):
    st.header(tr('Portfolio Analysis'))
    st.info(tr('Create and analyze your custom stock portfolio. Enter tickers and weights below.'))

    import yfinance as yf
    import pandas as pd
    import numpy as np
    import plotly.graph_objs as go
    from scipy.optimize import minimize
    import time

    # ==== Helpers for Analysis (compare mode) ====
    def _ms(t0: float) -> float:
        # Hitung elapsed time (ms) dari perf_counter start.
        return (time.perf_counter() - t0) * 1000.0

    def eval_portfolio(weights, mean_returns, cov_matrix, rf):
        w = np.asarray(weights)
        mu = float(np.dot(w, mean_returns))
        vol = float(np.sqrt(np.dot(w, cov_matrix @ w)))
        sharpe = (mu - rf) / vol if vol > 0 else np.nan
        return mu, vol, sharpe

    def solve_min_var(cov_matrix):
        n = cov_matrix.shape[0]
        w0 = np.repeat(1/n, n)
        bounds = [(0,1)] * n
        cons = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
        def obj(w): return np.sqrt(np.dot(w, cov_matrix @ w))
        res = minimize(obj, w0, bounds=bounds, constraints=cons)
        return res.x if res.success else w0

    def solve_max_sharpe(mean_returns, cov_matrix, rf):
        n = cov_matrix.shape[0]
        w0 = np.repeat(1/n, n)
        bounds = [(0,1)] * n
        cons = [{'type': 'eq', 'fun': lambda w: np.sum(w) - 1}]
        def neg_sharpe(w):
            mu = np.dot(w, mean_returns); vol = np.sqrt(np.dot(w, cov_matrix @ w))
            return - (mu - rf) / vol if vol > 0 else 1e9
        res = minimize(neg_sharpe, w0, bounds=bounds, constraints=cons)
        return res.x if res.success else w0

    def solve_erc(cov_matrix, iters=400, lr=0.01):
        n = cov_matrix.shape[0]
        w = np.repeat(1/n, n)
        for _ in range(iters):
            rc = w * (cov_matrix @ w)
            target = rc.sum() / n
            grad = (rc - target)
            w = np.clip(w - lr * grad, 0, 1)
            s = w.sum()
            w = np.repeat(1/n, n) if s == 0 else (w / s)
        return w

    def solve_equal_weight(n):  # HRP placeholder
        return np.repeat(1/n, n)

    # Jika Anda sudah punya ACO di analysis.py, siapkan import-nya:
    try:
        from analysis import aco_optimize_sharpe
    except Exception:
        aco_optimize_sharpe = None

    # Siapkan daftar metode yang bisa dibandingkan
    ALL_METHODS = [
        "Minimum Variance",
        "Maximum Sharpe Ratio",
        "Heuristic (ERC)",
        "Hierarchical Risk Parity (HRP)",  # placeholder = equal weight
        "Black-Litterman",
        "Ant Colony Optimization (ACO)"
    ]

    st.subheader(tr('Portfolio Formation Tool'))
    input_col, result_col = st.columns([1, 2])
    with input_col:
        method = st.selectbox(tr('Portfolio Construction Method'), ['Manual Weights', 'Minimum Variance', 'Maximum Sharpe Ratio', 'Hierarchical Risk Parity (HRP)', 'Heuristic (ERC)', 'Black-Litterman', 'Ant Colony Optimization (ACO)'])
        period = st.selectbox(tr('Historical Data Period'), ['1mo', '6mo', '1y', '3y', '5y', 'max'], index=2)
        rf_input = st.number_input(tr('Risk-free rate (annual, %)'), value=4.46, min_value=0.0, max_value=20.0, step=0.1, format="%.2f")
        rf = rf_input / 100.0
        tickers_input = st.text_input(tr('Enter stock tickers (comma separated)'), value='AAPL,MSFT,GOOGL')
        tickers = [t.strip().upper() for t in tickers_input.split(',') if t.strip()]
        weights = []

        # === Compare mode controls ===
        compare_mode = st.checkbox(tr('Compare multiple methods'))
        methods_to_compare = []
        if compare_mode:
            methods_to_compare = st.multiselect(
                tr('Select methods to compare'),
                ALL_METHODS,
                default=["Minimum Variance", "Maximum Sharpe Ratio", "Heuristic (ERC)"]
            )

        # --- defaults ACO: selalu didefinisikan ---
        aco_cfg = {"n_ants": 60,"n_iter": 200,"rho": 0.30,"alpha0": 60.0,"top_frac": 0.25,"seed": 42,}

        if method == 'Manual Weights':
            weights_input = st.text_input(tr('Enter weights (comma separated, must sum to 1)'), value='0.4,0.3,0.3')
            try:
                weights = [float(w) for w in weights_input.split(',') if w.strip()]
            except Exception:
                weights = []
    with result_col:
        try:
            data = yf.download(tickers, period=period, interval='1d', group_by='ticker', auto_adjust=True, progress=False)
        # Filter out invalid tickers (no data or all-NaN)
            valid_tickers = []
            for t in tickers:
                try:
                    close = data[t]['Close'] if t in data else None
                except Exception:
                    close = None
                if close is not None and close.dropna().shape[0] > 0:
                    valid_tickers.append(t)
            if len(valid_tickers) < len(tickers):
                dropped = list(set(tickers) - set(valid_tickers))
                st.warning(f"Dropped invalid tickers: {', '.join(dropped)}")
            if not valid_tickers:
                st.error('No valid tickers with price data. Please check your input.')
                st.stop()
            tickers = valid_tickers
            returns = pd.DataFrame({t: data[t]['Close'].pct_change().dropna() for t in tickers})
            mean_returns = returns.mean() * 252
            cov_matrix = returns.cov() * 252
            opt_runtime_ms = 0.0
            
            # === Compare mode execution (place BEFORE single-method branch) ===
            if compare_mode and methods_to_compare:
                results = []
                weight_maps = {}
                method_times = {}

                for m in methods_to_compare:
                    t0 = time.perf_counter()  # mulai timer untuk metode m
                    if m == "Minimum Variance":
                        w_m = solve_min_var(cov_matrix)
                    elif m == "Maximum Sharpe Ratio":
                        w_m = solve_max_sharpe(mean_returns, cov_matrix, rf)
                    elif m == "Heuristic (ERC)":
                        w_m = solve_erc(cov_matrix)
                    elif m == "Hierarchical Risk Parity (HRP)":
                        w_m = solve_equal_weight(len(mean_returns))
                    elif m == "Black-Litterman":
                        try:
                            caps = []
                            for t in tickers:
                                try:
                                    cap = yf.Ticker(t).info.get('marketCap', None)
                                    caps.append(cap if cap is not None else 1)
                                except Exception:
                                    caps.append(1)
                            caps = np.array(caps, dtype=float)
                            w_m = caps / caps.sum() if caps.sum() > 0 else solve_equal_weight(len(mean_returns))
                        except Exception:
                            w_m = solve_equal_weight(len(mean_returns))
                    elif m == "Ant Colony Optimization (ACO)":
                        if aco_optimize_sharpe is not None:
                            w_m, _ = aco_optimize_sharpe(mean_returns, cov_matrix, rf,
                                                        n_ants=60, n_iter=200, rho=0.30, alpha0=60.0,
                                                        top_frac=0.25, seed=42)
                        else:
                            w_m = solve_max_sharpe(mean_returns, cov_matrix, rf)
                    else:
                        w_m = solve_equal_weight(len(mean_returns))
                    runtime_ms = _ms(t0)    
                    method_times[m] = runtime_ms 

                    mu, vol, sh = eval_portfolio(w_m, mean_returns, cov_matrix, rf)
                    results.append({"Method": m, "Return": mu, "Volatility": vol, "Sharpe": sh,
                                    "Runtime (ms)": runtime_ms})
                    weight_maps[m] = pd.Series(w_m, index=tickers)

                # Tabel hasil
                df_res = pd.DataFrame(results).sort_values("Sharpe", ascending=False)
                st.subheader(tr('Comparison'))
                st.dataframe(
                    df_res.style.format({
                        "Return":"{:.2%}", "Volatility":"{:.2%}", "Sharpe":"{:.2f}", "Runtime (ms)":"{:.1f}"
                    }),
                    use_container_width=True
                )

                # Grafik batang Sharpe
                fig_cmp = go.Figure()
                fig_cmp.add_bar(x=df_res["Method"], y=df_res["Sharpe"])
                fig_cmp.update_layout(title=tr('Sharpe Ratio by Method'),
                                    xaxis_title=tr('Method'), yaxis_title=tr('Sharpe'))
                st.plotly_chart(fig_cmp, use_container_width=True)

                # Pie allocation untuk 3 metode teratas
                st.caption(tr('Top 3 allocations'))
                top_methods = df_res["Method"].head(3).tolist()
                cols = st.columns(len(top_methods))
                for col, m in zip(cols, top_methods):
                    with col:
                        s = weight_maps[m]
                        s = s[s > 0].sort_values(ascending=False).head(10)
                        fig_pie = go.Figure(data=[go.Pie(labels=s.index, values=s.values, hole=.35)])
                        fig_pie.update_layout(title=m)
                        st.plotly_chart(fig_pie, use_container_width=True)

                # Tabel bobot untuk tiap metode (compare)
                df_weights_all = pd.DataFrame({})

                for m, s in weight_maps.items():
                    df_weights_all[m] = s

                # Ubah ke persen
                df_weights_all = df_weights_all.applymap(lambda x: f"{x:.2%}")

                df_weights_all.index.name = tr('Ticker')
                st.subheader(tr('Portfolio Weights per Method'))
                st.dataframe(df_weights_all, use_container_width=True)

                st.caption(tr('Timing note: runtimes shown are for portfolio construction only (data loading not included).'))

                st.stop()  # hentikan agar cabang single-method di bawah tidak dieksekusi saat compare


            # Portfolio optimization
            if method == 'Manual Weights':
                t0 = time.perf_counter()
                valid = len(tickers) == len(weights) and np.isclose(sum(weights), 1.0)
                if not valid:
                    st.warning('Number of tickers and weights must match, and weights must sum to 1.')
                    st.stop()
                w = np.array(weights)
                opt_runtime_ms = _ms(t0)
            elif method == 'Minimum Variance':
                from scipy.optimize import minimize
                t0 = time.perf_counter()
                n = len(tickers)
                def port_vol(w):
                    return np.sqrt(np.dot(w, np.dot(cov_matrix, w)))
                cons = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
                bounds = tuple((0, 1) for _ in range(n))
                w0 = np.repeat(1/n, n)
                opt = minimize(port_vol, w0, bounds=bounds, constraints=cons)
                w = opt.x
                opt_runtime_ms = _ms(t0)
            elif method == 'Maximum Sharpe Ratio':
                from scipy.optimize import minimize
                t0 = time.perf_counter()
                n = len(tickers)
                def neg_sharpe(w):
                    port_ret = np.dot(w, mean_returns)
                    port_vol_ = np.sqrt(np.dot(w, np.dot(cov_matrix, w)))
                    return -(port_ret - rf) / port_vol_ if port_vol_ > 0 else 1e6
                cons = ({'type': 'eq', 'fun': lambda w: np.sum(w) - 1})
                bounds = tuple((0, 1) for _ in range(n))
                w0 = np.repeat(1/n, n)
                opt = minimize(neg_sharpe, w0, bounds=bounds, constraints=cons)
                w = opt.x
                opt_runtime_ms = _ms(t0)
            elif method == 'Hierarchical Risk Parity (HRP)':
                st.info('HRP is not yet implemented. Showing equal-weighted portfolio for now.')
                t0 = time.perf_counter()
                n = len(tickers)
                w = np.repeat(1/n, n)
                opt_runtime_ms = _ms(t0)
            elif method == 'Heuristic (ERC)':
                t0 = time.perf_counter()
                n = len(tickers)
                w = np.repeat(1/n, n)
                for _ in range(100):
                    risk_contrib = w * (cov_matrix @ w)
                    total_rc = np.sum(risk_contrib)
                    rc_target = total_rc / n
                    grad = (risk_contrib - rc_target)
                    w -= 0.01 * grad
                    w = np.clip(w, 0, 1)
                    w /= w.sum()
                opt_runtime_ms = _ms(t0)
                st.info('Heuristic: Equal Risk Contribution (ERC) portfolio.')
            elif method == 'Black-Litterman':
                st.info('Black-Litterman: using market cap weights as prior (no user views yet).')
                t0 = time.perf_counter()
                market_caps = []
                for t in tickers:
                    try:
                        cap = yf.Ticker(t).info.get('marketCap', None)
                        market_caps.append(cap if cap is not None else 1)
                    except Exception:
                        market_caps.append(1)
                market_caps = np.array(market_caps)
                if np.sum(market_caps) > 0:
                    w = market_caps / np.sum(market_caps)
                else:
                    w = np.repeat(1/len(tickers), len(tickers))
                opt_runtime_ms = _ms(t0)
                st.caption('Future version: allow custom user views for Black-Litterman.')
            elif method == 'Ant Colony Optimization (ACO)':
                with st.expander('ACO Settings (Advanced)', expanded=False):
                    aco_cfg["n_ants"]  = st.number_input(tr('Ants per iteration'), min_value=10,  max_value=500,  value=aco_cfg["n_ants"],  step=10)
                    aco_cfg["n_iter"]  = st.number_input(tr('Iterations'),        min_value=10,  max_value=3000, value=aco_cfg["n_iter"],  step=10)
                    aco_cfg["rho"]     = st.slider      (tr('Pheromone evaporation (rho)'), 0.05, 0.90, aco_cfg["rho"], 0.05)
                    aco_cfg["alpha0"]  = st.number_input(tr('Dirichlet concentration (alpha0)'), min_value=1.0, max_value=500.0, value=aco_cfg["alpha0"], step=1.0)
                    # Optional:
                    aco_cfg["top_frac"] = st.slider(tr('Top-ant fraction'), 0.05, 0.50, aco_cfg["top_frac"], 0.05)
                    aco_cfg["seed"]     = st.number_input(tr('Random seed'), min_value=0, max_value=10_000, value=aco_cfg["seed"], step=1)

                # ACO untuk memaksimalkan Sharpe Ratio
                with st.spinner('Running Ant Colony Optimization...'):
                    t0 = time.perf_counter()
                    w, best_sharpe = aco_optimize_sharpe(
                        mean_returns, cov_matrix, rf,
                        n_ants = int(aco_cfg["n_ants"]),
                        n_iter = int(aco_cfg["n_iter"]),
                        rho    = float(aco_cfg["rho"]),
                        alpha0 = float(aco_cfg["alpha0"]),
                        top_frac = float(aco_cfg["top_frac"]),
                        seed   = int(aco_cfg["seed"]),
                    )
                    opt_runtime_ms = _ms(t0)

                # Stats portofolio dari bobot terbaik
                port_return = np.dot(w, mean_returns)
                port_vol = np.sqrt(np.dot(w, np.dot(cov_matrix, w)))
                sharpe = (port_return - rf) / port_vol if port_vol > 0 else np.nan

            # Portfolio stats
            port_return = np.dot(w, mean_returns)
            port_vol = np.sqrt(np.dot(w, np.dot(cov_matrix, w)))
            sharpe = (port_return - rf) / port_vol if port_vol > 0 else np.nan

            # Show expected return and volatility as percentages, not currency
            st.success(f"{tr('Expected annual return:')} {port_return:.2%}")
            st.info(f"{tr('Expected annual volatility:')} {port_vol:.2%}")
            st.info(f"{tr('Sharpe Ratio (risk-free rate')} {rf_input:.2f}%): {sharpe:.2f}")
            st.caption(f"{tr('Optimization runtime')}: {opt_runtime_ms:.1f} ms")

            # Pie chart of weights
            fig = go.Figure(data=[go.Pie(labels=tickers, values=w, hole=.3)])
            fig.update_layout(title=tr('Portfolio Allocation'))
            st.plotly_chart(fig)
            
            df_weights = pd.DataFrame({
                tr('Ticker'): tickers,
                tr('Weight'): [f"{x:.2%}" for x in w]
            })
            st.subheader(tr('Portfolio Weights'))
            st.table(df_weights)        

        except Exception as e:
            st.warning(f'Could not fetch data or calculate portfolio: {e}')
        st.caption(tr('This tool uses historical data and allows several portfolio construction methods: Classic and Hybrid.'))

elif selected == tr('Sector Treemap'):
    import pandas as pd
    import streamlit as st
    from treemap import build_sector_treemap

    st.header(tr('Sector Treemap'))
    st.info(tr('Visualize one stock index grouped by sector.'))

    # --- Pilih indeks (contoh: subset LQ45 / S&P 100). Ganti/extend sesuai kebutuhan. ---
    INDEX_MAP = {
        "IDX LQ45 (example subset)": [
            "BBCA.JK","BBRI.JK","BMRI.JK","BBNI.JK","ASII.JK","TLKM.JK",
            "UNVR.JK","ICBP.JK","INDF.JK","UNTR.JK","HMSP.JK","SMGR.JK",
            "INTP.JK","MDKA.JK","ANTM.JK","INCO.JK","ADRO.JK","PTBA.JK"
        ],
        "S&P 100 (example subset)": [
            "AAPL","MSFT","GOOGL","AMZN","META","TSLA",
            "BRK-B","JNJ","JPM","XOM","PG","NVDA","UNH","V","HD"
        ],
    }

    # --- Panel input ---
    left, right = st.columns([1,2])
    with left:
        index_choice = st.selectbox(tr('Select index'), list(INDEX_MAP.keys()))
        use_custom_range = st.checkbox(tr('Use custom date range'))
        # period default bila tidak custom
        period = st.selectbox(tr('Historical Data Period'),
                              ['1d','1w','1mo','3mo','6mo','1y','3y','5y','max'], index=4,
                              disabled=use_custom_range)
        # custom date range
        today = pd.Timestamp.today().normalize()
        default_start = today - pd.DateOffset(months=6)
        start_date, end_date = None, None
        if use_custom_range:
            date_range = st.date_input(tr('Select date range'),
                                       value=(default_start.date(), today.date()))
            if isinstance(date_range, tuple) and len(date_range) == 2:
                start_date, end_date = date_range
                if start_date >= end_date:
                    st.warning(tr('Invalid date range: start must be before end'))
                    start_date, end_date = None, None
                elif end_date > today.date():
                    st.warning(f"{tr('End date beyond today. Data will be cut off at')} {today.date()}.")
                    end_date = today.date()
            else:
                st.warning(tr('Please select both start and end dates'))

        tickers_index = INDEX_MAP[index_choice]
        st.caption(tr('Tickers in index:') + " " + ", ".join(tickers_index))

    with right:
        try:
            with st.spinner(tr('Loading treemap...')):
                if use_custom_range:
                    if not start_date or not end_date:
                        st.warning(tr('Please select both start and end dates'))
                        st.stop()
                    # custom range: TIDAK auto-adjust weekend → bila kosong, raise warning
                    fig, df_meta = build_sector_treemap(
                        tickers_index,
                        start=pd.to_datetime(start_date),
                        end=pd.to_datetime(end_date)
                    )
                    st.caption(tr('Data range:') + f" {start_date} → {end_date}")
                    plot_key = f"treemap_custom_{index_choice}_{start_date}_{end_date}"
                else:
                    # preset: include_today=True agar data sampai hari ini (seperti Stock Overview)
                    fig, df_meta = build_sector_treemap(
                        tickers_index,
                        period=period,
                        include_today=True
                    )
                    st.caption(tr('Period:') + f" {period}")
                    plot_key = f"treemap_period_{index_choice}_{period}"

            st.plotly_chart(fig, use_container_width=True, key=plot_key)

            st.subheader(tr('Constituents snapshot'))
            show_df = df_meta.copy()
            show_df["Perf"] = show_df["Perf"].map(lambda x: f"{x*100:.2f}%")
            st.dataframe(show_df[["Ticker","Sector","MarketCap","Perf"]], use_container_width=True, key=f"df_{plot_key}")

            st.caption(tr('Size = Market Cap, Color = Performance (green up, red down).'))

        except ValueError as e:
            msg = str(e)
            if msg == "NO_TRADING_DATA":
                st.warning(tr('No trading data in the selected date range (likely weekend/holiday). Please pick a range that includes trading days.'))
            elif msg == "NOT_ENOUGH_TRADING_DAYS":
                st.warning(tr('Not enough trading days in the selected range to compute performance. Please expand the range.'))
            else:
                st.error(tr('Unexpected error while building treemap.'))

elif selected == tr("About Us"):
    about_page()