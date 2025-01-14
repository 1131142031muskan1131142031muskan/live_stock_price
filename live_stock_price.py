import streamlit as st
import pandas as pd
import requests
from bs4 import BeautifulSoup
from streamlit_autorefresh import st_autorefresh

# Title of the app
st.title("Live Stock Price Tracker")

# Sidebar for user input
ticker = st.sidebar.text_input("Enter Stock Symbol", "INFY")
exchange = st.sidebar.text_input("Enter Exchange", "NSE")

# Function to fetch stock price
def fetch_stock_price(symbol, exchange_name):
    url = f"https://www.google.com/finance/quote/{symbol}:{exchange_name}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    try:
        # Extract stock price
        price = float(soup.find(class_="rPF6Lc").text.strip()[1:].replace(",", ""))
        return price
    except Exception:
        return None
# Fetch and display the stock price
stock_price = fetch_stock_price(ticker, exchange)

if stock_price:
    st.metric("Current Stock Price", f"₹{stock_price}")
else:
    st.error("Could not fetch stock price. Please check the symbol and exchange.")

# Auto-refresh every 10 seconds (10000 milliseconds)
st_autorefresh(interval=10000)