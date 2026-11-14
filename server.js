const express = require('express');
const fs = require('fs');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;
const DB_FILE = path.join(__dirname, 'database.json');

app.use(express.json({ limit: '10mb' }));
app.use(express.static(__dirname));

// Rota para ler o banco de dados
app.get('/api/db', (req, res) => {
    if (fs.existsSync(DB_FILE)) {
        res.sendFile(DB_FILE);
    } else {
        res.json({ stores: {} });
    }
});

// Rota para salvar o banco de dados
app.post('/api/db', (req, res) => {
    fs.writeFile(DB_FILE, JSON.stringify(req.body, null, 2), (err) => {
        if (err) {
            res.status(500).send("Erro ao salvar dados");
        } else {
            res.send("Salvo com sucesso");
        }
    });
});

app.listen(PORT, () => {
    console.log(`Servidor rodando na porta ${PORT}`);
});