const express = require('express');
const fetch = require('node-fetch');
const NodeCache = require('node-cache');

const app = express();
const PORT = 4000;

const myCache = new NodeCache({ stdTTL: 100, checkperiod: 120 });

let roundRobinCounter = {
  "catalog-service": 0,
  "cart-service": 0
};

const catalogReplicas = [
  "http://localhost:5000",
  "http://localhost:5002",
  "http://localhost:5003",
  "http://localhost:5004"
];

const cartReplicas = [
  "http://localhost:5001",
  "http://localhost:5005",
  "http://localhost:5006",
  "http://localhost:5007"
];

function getNextReplica(serviceName) {
    let replicas;
    if (serviceName === "catalog-service") {
        replicas = catalogReplicas;
    } else if (serviceName === "cart-service") {
        replicas = cartReplicas;
    }
    const index = roundRobinCounter[serviceName] % replicas.length;
    roundRobinCounter[serviceName]++;
    return replicas[index];
}

app.use(express.json());

app.get('/status', (req, res) => {
    res.json({ status: "Gateway is healthy" });
});

app.get('/items', async (req, res) => {
    const CATALOG_SERVICE = getNextReplica("catalog-service");
    
    const cachedData = myCache.get("items");
    if (cachedData) {
        return res.json(cachedData);
    }

    try {
        const response = await fetch(`${CATALOG_SERVICE}/items`);
        const data = await response.json();
        myCache.set("items", data);
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: "Failed to fetch from Catalog Service" });
    }
});

app.post('/add', async (req, res) => {
    const CART_SERVICE = getNextReplica("cart-service");
    
    try {
        const response = await fetch(`${CART_SERVICE}/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(req.body)
        });
        const data = await response.json();
        res.json(data);
    } catch (error) {
        res.status(500).json({ error: "Failed to forward request to Cart Service" });
    }
});

app.listen(PORT, () => {
    console.log(`Gateway is running on http://localhost:${PORT}`);
});



// Service Registry Registration:
// Endpoint: http://localhost:3000/register
// HTTP Method: POST
// Body (raw + JSON):
// {
//     "name": "catalog-service",
//     "host": "localhost",
//     "port": 5000
// }
// This will register the catalog service with the service registry.

// Service Discovery:
// Endpoint: http://localhost:3000/discover/catalog-service
// HTTP Method: GET
// This request fetches details about the catalog service from the registry.

// Add Item to Cart:
// Endpoint: http://localhost:5001/add
// HTTP Method: POST
// Body (raw + JSON):
// {
//     "item": "laptop",
//     "quantity": 2
// }
// This request will attempt to add 2 laptops to the cart.

// Fetch Catalog Items:
// Endpoint: http://localhost:5000/items
// HTTP Method: GET
// This request fetches all items from the catalog service.

// Service Status Check:
// Endpoint for cart service: http://localhost:5001/status
// Endpoint for catalog service: http://localhost:5000/status
// HTTP Method: GET
// These requests check if the respective services are running and healthy.

// Gateway Status Check:
// Endpoint: http://localhost:4000/status
// HTTP Method: GET
// This request checks the health of the gateway.

// Service Status from Gateway:
// Endpoint: http://localhost:4000/services-status
// HTTP Method: GET
// This request fetches the health of all services via the gateway.

// Get Items through Gateway with Caching:
// Endpoint: http://localhost:4000/items
// HTTP Method: GET
// This request fetches items from the catalog service through the gateway and utilizes caching.

// Add Item to Cart through Gateway:
// Endpoint: http://localhost:4000/add
// HTTP Method: POST
// Body (raw + JSON):
// {
//     "item": "phone",
//     "quantity": 3
// }