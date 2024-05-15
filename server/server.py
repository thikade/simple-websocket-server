#!/usr/bin/env python

# source: https://websockets.readthedocs.io/en/stable/howto/quickstart.html

import asyncio
import os
import signal

import websockets


async def echo(websocket):
    async for message in websocket:
        await websocket.send(message + " (from your Python websocket-server :-)")


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve( echo, host="localhost", port=8000 ):
        await stop


if __name__ == "__main__":
    asyncio.run(main())