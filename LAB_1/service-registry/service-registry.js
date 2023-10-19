const express = require('express');
const app = express();
const PORT = 3000;

let services = {};

app.use(express.json());

app.post('/register', (req, res) => {
    const { name, host, port } = req.body;
    const key = `${name}-${host}:${port}`;
    services[key] = { name, host, port };
    res.send({ success: true });
});

app.get('/discover/:name', (req, res) => {
    const serviceNames = Object.keys(services).filter(key => services[key].name === req.params.name);
    if (!serviceNames.length) {
        return res.status(404).send({ error: 'Service not found' });
    }
    // Implementing Round Robin for Load Balancing
    const nextService = serviceNames.shift();
    serviceNames.push(nextService);
    res.send(services[nextService]);
});

app.get('/status', (req, res) => {
    res.send({ status: 'Service Registry is up', services });
});

app.listen(PORT, () => {
    console.log(`Service Registry running on http://localhost:${PORT}`);
});
