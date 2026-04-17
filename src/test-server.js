const http = require('http');
const fs = require('fs');
const path = require('path');
const os = require('os');

// Read configuration to get the port
const configPath = path.join(os.homedir(), '.config', 'civil-server.json');
let port = 3333; // default

try {
    if (fs.existsSync(configPath)) {
        const configData = fs.readFileSync(configPath, 'utf8');
        const config = JSON.parse(configData);
        port = parseInt(config.port) || 3333;
    }
} catch (error) {
    console.log('Using default port 3333 due to config error:', error.message);
}

// Allow command line override
if (process.argv[2]) {
    port = parseInt(process.argv[2]) || port;
}

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
