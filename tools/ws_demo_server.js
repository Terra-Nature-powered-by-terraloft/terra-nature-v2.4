const WebSocket = require('ws');
const crypto = require('crypto');

function randomPayload() {
  return JSON.stringify({
    type: 'NRG',
    value: Math.random(),
    id: crypto.randomUUID()
  });
}

function createServer({ port = 8765 } = {}) {
  const wss = new WebSocket.Server({ port });
  wss.on('connection', (ws) => {
    ws.send(randomPayload());
    const interval = setInterval(() => ws.send(randomPayload()), 1000);
    ws.on('close', () => clearInterval(interval));
  });
  return wss;
}

if (require.main === module) {
  const port = process.env.PORT ? parseInt(process.env.PORT, 10) : 8765;
  createServer({ port });
  console.log(`WS demo server running on ws://localhost:${port}`);
}

module.exports = { createServer };
