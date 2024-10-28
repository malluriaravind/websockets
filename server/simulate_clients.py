#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WebSocket Server: Appends a random number to each incoming message.
"""

import asyncio
from random import randint
from websockets.server import serve

async def echo(websocket):
    async for message in websocket:
        # Append a random number to the message
        modified_message = f"[{randint(1, 100)}] {message}"
        await websocket.send(modified_message)

async def main():
    # Start the WebSocket server
    async with serve(echo, "localhost", 8765):
        await asyncio.Future()  # run forever

asyncio.run(main())
