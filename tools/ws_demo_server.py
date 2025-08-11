import asyncio
import json
import os
import random
import uuid
import websockets


def random_payload():
    return json.dumps({
        "type": "NRG",
        "value": random.random(),
        "id": str(uuid.uuid4()),
    })


async def handler(websocket):
    try:
        await websocket.send(random_payload())
        while True:
            await asyncio.sleep(1)
            await websocket.send(random_payload())
    except websockets.ConnectionClosed:
        pass


async def start_server(host="localhost", port=8765):
    return await websockets.serve(handler, host, port)


async def serve(host="localhost", port=8765):
    async with await start_server(host, port):
        print(f"WS demo server running on ws://{host}:{port}")
        await asyncio.Future()


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8765))
    asyncio.run(serve(port=port))
