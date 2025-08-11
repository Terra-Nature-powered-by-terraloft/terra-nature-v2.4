const assert = require('assert');
const { once } = require('events');
const WebSocket = require('ws');
const { createServer } = require('../tools/ws_demo_server.js');
const test = require('node:test');

test('ws_demo_server.js emits NRG payload', async () => {
  const server = createServer({ port: 0 });
  await once(server, 'listening');
  const port = server.address().port;

  const ws = new WebSocket(`ws://localhost:${port}`);
  const [message] = await once(ws, 'message');
  ws.close();
  server.close();

  const payload = JSON.parse(message);
  assert.equal(payload.type, 'NRG');
  assert.equal(typeof payload.value, 'number');
});
