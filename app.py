from flask import Flask, render_template, request, jsonify
import requests
import csv
from datetime import datetime
import os

app = Flask(__name__)

API_KEY = '7TAV316NEGWAT286' # Isey apni real key se replace zaroor kariyega

# Function to save search to CSV
def backup_search(symbol, price, change):
    file_exists = os.path.isfile('search_history.csv')
    
    with open('search_history.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        # Agar file nayi hai toh header likhen
        if not file_exists:
            writer.writerow(['Timestamp', 'Symbol', 'Price', 'Change'])
        
        # Current time aur data save karein
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        writer.writerow([timestamp, symbol, price, change])

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_stock', methods=['POST'])
def get_stock():
    symbol = request.json.get('symbol')
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if "Global Quote" in data and data["Global Quote"]:
            quote = data["Global Quote"]
            
            # --- BACKUP LOGIC START ---
            price = quote.get('05. price')
            change = quote.get('09. change')
            backup_search(symbol, price, change)
            # --- BACKUP LOGIC END ---
            
            return jsonify(quote)
        else:
            return jsonify({"error": "Stock not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)