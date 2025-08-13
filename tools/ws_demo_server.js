const http = require('http');
const fs = require('fs');
const path = require('path');

const publicDir = path.join(__dirname, '..', 'public');

const server = http.createServer((req, res) => {
  // Sanitize the URL to prevent path traversal
  const requestedPath = req.url === '/' ? 'dashboard.html' : req.url.replace(/^\/+/, '');
  const normalizedPath = path.normalize(requestedPath);
  const filePath = path.join(publicDir, normalizedPath);

  // Ensure the resolved path is within publicDir
  if (!filePath.startsWith(publicDir)) {
    res.writeHead(403);
    res.end('Forbidden');
    return;
  }
  const ext = path.extname(filePath);
  let contentType = 'text/html';
  if (ext === '.css') contentType = 'text/css';

  fs.readFile(filePath, (err, content) => {
    if (err) {
      res.writeHead(404);
      res.end('Not found');
      return;
    }
    res.writeHead(200, { 'Content-Type': contentType });
    res.end(content);
  });
});

const port = 8000;
server.listen(port, () => {
  console.log(`Serving ${publicDir} on http://localhost:${port}`);
});
