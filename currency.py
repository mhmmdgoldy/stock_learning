# currency.py - Currency selection and conversion helpers for Streamlit Finance Webapp

import streamlit as st

# Supported currencies and symbols
CURRENCIES = {
    'USD': {'symbol': '$', 'name': 'US Dollar'},
    'IDR': {'symbol': 'Rp', 'name': 'Indonesian Rupiah'},
}

# Set or get currency in session_state

def set_currency(currency_code):
    st.session_state['currency'] = currency_code

def get_currency():
    return st.session_state.get('currency', 'USD')

# Return currency symbol for current selection
def currency_symbol():
    code = get_currency()
    return CURRENCIES.get(code, {}).get('symbol', '')

# Live/offline conversion using CurrencyConverter
from currency_converter import CurrencyConverter

cc = CurrencyConverter()
def convert(amount, from_cur, to_cur):
    if from_cur == to_cur:
        return amount
    try:
        return cc.convert(amount, from_cur, to_cur)
    except Exception:
        # fallback: return original amount if conversion fails
        return amount
