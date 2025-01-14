
from flask import Flask, jsonify, request
import requests
from bs4 import BeautifulSoup

# Initialize Flask app
app = Flask(__name__)  # Correct syntax for Flask initialization

# API Route: Fetch stock price
@app.route('/get_stock_price', methods=['GET'])
def get_stock_price():
    # Get parameters from the request
    ticker = request.args.get('ticker', 'INFY')  # Default ticker: INFY
    exchange = request.args.get('exchange', 'NSE')  # Default exchange: NSE

    # Construct the URL
    url = f"https://www.google.com/finance/quote/{ticker}:{exchange}"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    try:
        # Extract stock price
        price = float(soup.find(class_="rPF6Lc").text.strip()[1:].replace(",", ""))
        return jsonify({'ticker': ticker, 'exchange': exchange, 'price': price})
    except Exception as e:
        # Return an error message if something goes wrong
        return jsonify({'error': 'Failed to fetch stock price', 'details': str(e)})

# Start the Flask server
if __name__ == '__main__':
    app.run(debug=True)










