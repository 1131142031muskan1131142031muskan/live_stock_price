import streamlit as st
from flask import Flask, jsonify, request
from bs4 import BeautifulSoup
import threading
import requests

# Initialize Flask app
flask_app = Flask(_name_)

# Flask API: Fetch stock price
@flask_app.route('/get_stock_price', methods=['GET'])
def get_stock_price():
    ticker = request.args.get('ticker', 'INFY')  # Default ticker: INFY
    exchange = request.args.get('exchange', 'NSE')  # Default exchange: NSE
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    try:
        price = float(soup.find(class_="rPF6Lc").text.strip()[1:].replace(",", ""))
        return jsonify({'ticker': ticker, 'exchange': exchange, 'price': price})
    except Exception as e:
        return jsonify({'error': 'Failed to fetch stock price', 'details': str(e)})

# Run Flask API in a separate thread
def run_flask():
    flask_app.run(port=5000, debug=False, use_reloader=False)

threading.Thread(target=run_flask).start()

# Streamlit App: Live Stock Price Tracker
st.title("Live Stock Price Tracker")

# Sidebar Inputs
ticker = st.sidebar.text_input("Enter Stock Ticker Symbol (e.g., INFY)", "INFY")
exchange = st.sidebar.text_input("Enter Exchange (e.g., NSE)", "NSE")

# API URL (internal Flask API)
api_url = f"http://127.0.0.1:5000/get_stock_price?ticker={ticker}&exchange={exchange}"

# Fetch Stock Price
try:
    response = requests.get(api_url)
    if response.status_code == 200:
        data = response.json()
        if "price" in data:
            st.subheader("Current Stock Price")
            st.write(f"The stock price of {data['ticker']} on {data['exchange']} is: ₹{data['price']}")
        else:
            st.error(data.get("error", "Unknown error occurred"))
    else:
        st.error(f"API request failed with status code {response.status_code}")
except Exception as e:
    st.error(f"Error connecting to the API: {str(e)}"
'''import streamlit as st
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
    st.metric("Current Stock Price", f"₹{stock_price}")'''
else:
    st.error("Could not fetch stock price. Please check the symbol and exchange.")

# Auto-refresh every 10 seconds (10000 milliseconds)
st_autorefresh(interval=10000)
