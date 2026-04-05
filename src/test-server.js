const http = require('http');

const port = process.argv[2] || 3333;

const server = http.createServer((req, res) => {
    res.writeHead(200, { 'Content-Type': 'text/html' });
    res.end(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>Civil Server Test</title>
            <style>
                body { 
                    font-family: Arial, sans-serif;
                    background: #2c3e50;
                    color: white;
                    text-align: center;
                    padding: 50px;
                }
                .container {
                    max-width: 600px;
                    margin: 0 auto;
                    background: #34495e;
                    padding: 30px;
                    border-radius: 10px;
                }
                h1 { color: #3498db; }
                .status {
                    background: #27ae60;
                    padding: 10px;
                    border-radius: 5px;
                    margin: 20px 0;
                }
                .port-info {
                    background: #e74c3c;
                    padding: 10px;
                    border-radius: 5px;
                    margin: 20px 0;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Civil Server Test</h1>
                <div class="status">✅ Server Running</div>
                <div class="port-info">Port: ${port}</div>
                <p>This is a test server started by Civil Server.</p>
            </div>
        </body>
        </html>
    `);
});

server.listen(port, () => {
    console.log(`Test server running on http://localhost:${port}`);
});
