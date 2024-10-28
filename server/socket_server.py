#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Simulates 10,000 WebSocket clients connecting to the server.
"""

import asyncio
import logging
from websockets import connect

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

async def client_task(client_id, messages_received):
    uri = "ws://localhost:8765"
    try:
        async with connect(uri) as websocket:
            # Send message to the server
            message = f"Client {client_id} says hello!"
            await websocket.send(message)
            logging.info(f"Client {client_id}: Sent: {message}")

            # Receive the modified message from the server
            response = await websocket.recv()
            logging.info(f"Client {client_id}: Received: {response}")
            messages_received.append((client_id, message, response))
    except Exception as e:
        logging.error(f"Client {client_id}: Error: {e}")

async def main():
    total_clients = 10000  # Total number of simulated clients
    batch_size = 500       # Number of concurrent clients per batch
    delay_between_batches = 1  # Seconds to wait between batches

    messages_received = []  # To store messages for verification

    for batch_start in range(0, total_clients, batch_size):
        tasks = []
        batch_end = min(batch_start + batch_size, total_clients)
        for client_id in range(batch_start + 1, batch_end + 1):
            task = asyncio.create_task(client_task(client_id, messages_received))
            tasks.append(task)
        logging.info(f"Initiated clients {batch_start + 1} to {batch_end}")
        await asyncio.gather(*tasks)
        logging.info(f"Completed clients {batch_start + 1} to {batch_end}")
        await asyncio.sleep(delay_between_batches)  # Prevent overwhelming the server

    logging.info("All clients have been processed.")
    if len(messages_received) == total_clients:
        logging.info("Success: All messages received.")
    else:
        logging.warning(f"Warning: Only {len(messages_received)} out of {total_clients} messages received.")

if __name__ == "__main__":
    asyncio.run(main())
