from flask import Flask, jsonify, request
import json
import requests
from circuit_breaker import CircuitBreaker

app = Flask(__name__)
cb = CircuitBreaker()

def load_db():
    with open('catalog_db.json', 'r') as f:
        return json.load(f)

def save_db(catalog):
    with open('catalog_db.json', 'w') as f:
        json.dump(catalog, f)



@app.route('/add-item', methods=['POST'])
@with_circuit_breaker
def add_item():
    item = request.json.get('item')
    price = request.json.get('price')
    quantity = request.json.get('quantity', 1)  # default to 1 if not provided

    if not item or not price:
        return jsonify({'error': 'Item name or price is missing'}), 400

    items = load_db()

    # If item already exists, update its quantity
    if item in items:
        existing_item = items[item]
        if 'quantity' in existing_item:
            existing_item['quantity'] += quantity
        else:
            existing_item['quantity'] = quantity
        existing_item['price'] = price  # update price as well
    else:
        # If item does not exist, add it
        items[item] = {'price': price, 'quantity': quantity}

    save_db(items)

    return jsonify(items[item]), 201

@app.route('/items', methods=['GET'])
@with_circuit_breaker
def get_items():
    items = load_db()
    return jsonify(items), 200

@app.route('/status', methods=['GET'])
def status():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(port=5000)
