const http = require('http');
const fs = require('fs');
const path = require('path');

const server = http.createServer((req, res) => {
    let filePath = path.join(__dirname, req.url === '/' ? 'life-saas-interface.html' : req.url);

    fs.readFile(filePath, (err, data) => {
        if (err) {
            res.writeHead(404);
            res.end('File not found');
            return;
        }

        const ext = path.extname(filePath);
        let contentType = 'text/html';

        if (ext === '.css') contentType = 'text/css';
        if (ext === '.js') contentType = 'text/javascript';

        res.writeHead(200, {
            'Content-Type': contentType,
            'Cache-Control': 'no-cache, no-store, must-revalidate'
        });
        res.end(data);
    });
});

server.listen(8001, () => {
    console.log('Server running on http://localhost:8001');
});