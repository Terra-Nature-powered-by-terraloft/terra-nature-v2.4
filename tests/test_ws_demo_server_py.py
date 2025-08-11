import asyncio
import json

import pytest
import websockets

import tools.ws_demo_server as ws_demo_server


@pytest.mark.asyncio
async def test_ws_demo_server_py():
    server = await ws_demo_server.start_server(port=0)
    port = server.sockets[0].getsockname()[1]

    async with websockets.connect(f"ws://localhost:{port}") as ws:
        message = await ws.recv()
        payload = json.loads(message)
        assert payload["type"] == "NRG"
        assert isinstance(payload["value"], float)

    server.close()
    await server.wait_closed()
