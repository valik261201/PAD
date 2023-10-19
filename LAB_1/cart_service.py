from flask import Flask, jsonify, request
import json
import requests
from circuit_breaker import CircuitBreaker
from threading import Semaphore

app = Flask(__name__)
CATALOG_URL = "http://localhost:5000/items"
CONCURRENT_TASKS_LIMIT = 5
semaphore = Semaphore(CONCURRENT_TASKS_LIMIT)
cb = CircuitBreaker()

def load_cart():
    with open('cart_db.json', 'r') as f:
        return json.load(f)

def save_cart(cart):
    with open('cart_db.json', 'w') as f:
        json.dump(cart, f)

@app.route('/add', methods=['POST'])
def add_to_cart():
    with semaphore:
        cart = load_cart()
        item = request.json.get('item')
        quantity = request.json.get('quantity', 1)

        response = cb.call(requests.get, f"{CATALOG_URL}/{item}")  # Request specific item using Circuit Breaker

        if response.status_code == 200:
            catalog_item = response.json().get(item)
            if not catalog_item:
                return jsonify({'error': 'Item not found in catalog'}), 404
            
            if item in cart:
                cart[item] += quantity
            else:
                cart[item] = quantity

            save_cart(cart)
            return jsonify(cart), 200
        else:
            return jsonify({'error': 'Unable to fetch catalog'}), 500

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(port=5001)
