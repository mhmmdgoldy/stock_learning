# Stock Website

A Streamlit-based finance web application for stock analysis, portfolio construction, and Syariah compliance screening with full multi-language (English/Bahasa Indonesia) and multi-currency support.

## Features
- `Stock Overview`: Visualize stock prices, general info, and fundamentals for any ticker (supports global stocks and IDX).
- `Syariah Stock Screening`: Check Syariah (Sharia) compliance for stocks using OJK/HISSA-like criteria, with localized criteria and sector/industry translation.
- `Portfolio Analysis`: Build and analyze custom portfolios with various construction methods (Manual, Min-Var, Max Sharpe, Black-Litterman, ERC, HRP placeholder).
- `Multi-Language`: All UI, static, and dynamic content fully translatable (English & Bahasa Indonesia).
- `Multi-Currency`: All monetary values shown in the stock's native currency, with optional conversion to user-selected currency (USD/IDR) using live rates.
- `Simple UI`: Responsive, clean Streamlit interface.

## Getting Started

### Requirements
Install dependencies:
```bash
pip install -r requirements.txt
```

### Run the App
```bash
streamlit run app.py
```

### Configuration
- No API keys required for basic features (uses Yahoo Finance and ECB rates).

## Project Structure
- `app.py` - Main Streamlit app
- `i18n.py` - Internationalization (translation) logic
- `currency.py` - Currency selection and conversion logic
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.

---

### MIT License

Copyright (c) 2025 Muhammad Goldy

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
