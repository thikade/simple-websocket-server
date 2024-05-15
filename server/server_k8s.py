#!/usr/bin/env python

# source: https://websockets.readthedocs.io/en/stable/howto/kubernetes.html

import asyncio
import http
import signal
import sys
import time

import websockets


async def echo(websocket):
    async for message in websocket:
        await websocket.send(message + " (from your K8s websocket-server :-)")


async def health_check(path, request_headers):
    if path == "/healthz":
        return http.HTTPStatus.OK, [], b"OK\n"
    if path == "/inemuri":
        loop = asyncio.get_running_loop()
        loop.call_later(1, time.sleep, 10)
        return http.HTTPStatus.OK, [], b"Sleeping for 10s\n"
    if path == "/seppuku":
        loop = asyncio.get_running_loop()
        loop.call_later(1, sys.exit, 69)
        return http.HTTPStatus.OK, [], b"Terminating\n"


async def main():
    # Set the stop condition when receiving SIGTERM.
    loop = asyncio.get_running_loop()
    stop = loop.create_future()
    loop.add_signal_handler(signal.SIGTERM, stop.set_result, None)

    async with websockets.serve(
        echo,
        host="",
        port=8000,
        process_request=health_check,
    ):
        await stop


if __name__ == "__main__":
    asyncio.run(main())