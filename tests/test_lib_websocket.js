const test = require('node:test');
const assert = require('assert');
const { WebSocketClient, createClient } = require('../lib/websocket');

test('lib/websocket module exports work correctly', () => {
  // Test WebSocketClient class export
  assert(typeof WebSocketClient === 'function', 'WebSocketClient should be a function');
  
  // Test createClient factory function
  assert(typeof createClient === 'function', 'createClient should be a function');
  
  const client = createClient();
  assert(client instanceof WebSocketClient, 'createClient should return WebSocketClient instance');
});

test('WebSocketClient basic functionality', async () => {
  const client = new WebSocketClient();
  
  // Test initial state
  assert.equal(client.isConnected(), false, 'Client should not be connected initially');
  
  // Test connect method
  const connection = await client.connect('ws://localhost:8080');
  assert.equal(client.isConnected(), true, 'Client should be connected after connect()');
  assert.equal(client.url, 'ws://localhost:8080', 'URL should be stored correctly');
  
  // Test send method
  assert.doesNotThrow(() => {
    client.send('test message');
  }, 'send() should not throw when connected');
  
  // Test close method
  client.close();
  assert.equal(client.isConnected(), false, 'Client should not be connected after close()');
  
  // Test send method after close
  assert.throws(() => {
    client.send('test message');
  }, 'send() should throw when not connected');
});

test('WebSocketClient event handling', async () => {
  const client = new WebSocketClient();
  let connectCalled = false;
  let messageCalled = false;
  let closeCalled = false;
  
  // Add event listeners
  client.on('connect', () => { connectCalled = true; });
  client.on('message', () => { messageCalled = true; });
  client.on('close', () => { closeCalled = true; });
  
  // Test connect event
  await client.connect('ws://test');
  assert.equal(connectCalled, true, 'connect event should be fired');
  
  // Test message event
  client.send('test');
  assert.equal(messageCalled, true, 'message event should be fired');
  
  // Test close event
  client.close();
  assert.equal(closeCalled, true, 'close event should be fired');
});