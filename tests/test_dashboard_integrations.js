const assert = require('assert');
const fs = require('fs');
const path = require('path');
const { once } = require('events');
const WebSocket = require('ws');
const test = require('node:test');

const ROOT = path.join(__dirname, '..');

function readProjectFile(relativePath) {
  const absolutePath = path.join(ROOT, relativePath);
  return fs.readFileSync(absolutePath, 'utf8');
}

test('Terra Nature dashboard references TerraBrand fonts', () => {
  const layoutContent = readProjectFile('app/layout.tsx');
  const componentContent = readProjectFile('components/TerraNatureDashboardV2Live.tsx');

  assert(/TerraBrand\s+Sans/.test(layoutContent), 'Layout should declare TerraBrand Sans font');
  assert(/TerraBrand\s+Serif/.test(layoutContent), 'Layout should declare TerraBrand Serif font');
  assert(/TerraBrand\s+Sans/.test(componentContent), 'Dashboard component should use TerraBrand Sans font family');
});

test('NRG NFT template CSV can be ingested', () => {
  const csvContent = readProjectFile('data/nrg_nft_events_template.csv').trim();
  const [headerLine, ...rows] = csvContent.split(/\r?\n/);
  const headers = headerLine.split(',');

  assert.deepStrictEqual(headers, ['timestamp', 'id', 'energy_kwh', 'co2_kg', 'miner', 'proof']);
  assert(rows.length > 0, 'CSV should include at least one data row');

  const parsedRows = rows.map((row) => {
    const values = row.split(',');
    return headers.reduce((record, header, index) => {
      record[header] = values[index];
      return record;
    }, {});
  });

  for (const record of parsedRows) {
    assert.ok(record.timestamp, 'timestamp should be present');
    assert.ok(record.id, 'id should be present');
    assert.ok(record.miner, 'miner should be present');
    assert.ok(record.proof, 'proof should be present');
    assert(!Number.isNaN(Number.parseFloat(record.energy_kwh)), 'energy_kwh should parse to a number');
    assert(!Number.isNaN(Number.parseFloat(record.co2_kg)), 'co2_kg should parse to a number');
  }
});

test('Demo WebSocket server streams Terra Nature events', async () => {
  const { createServer } = require('../tools/ws_demo_server.js');

  const server = createServer({ port: 0 });
  await once(server, 'listening');
  const port = server.address().port;

  const ws = new WebSocket(`ws://localhost:${port}`);
  const [firstMessage] = await once(ws, 'message');
  const [secondMessage] = await once(ws, 'message');
  ws.close();
  server.close();

  const firstPayload = JSON.parse(firstMessage);
  const secondPayload = JSON.parse(secondMessage);

  assert.equal(firstPayload.type, 'NRG');
  assert.equal(typeof firstPayload.value, 'number');
  assert.ok(firstPayload.id, 'payload should include id field');

  assert.equal(secondPayload.type, 'NRG');
  assert.equal(typeof secondPayload.value, 'number');
  assert.ok(secondPayload.id, 'second payload should include id field');

  assert.notEqual(firstPayload.id, secondPayload.id, 'streamed events should have unique ids');
});
