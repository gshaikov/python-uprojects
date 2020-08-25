import asyncio
import re
import logging
from typing import Tuple, Optional
from contextlib import asynccontextmanager
from functools import wraps
from urllib.parse import urlparse


logging.basicConfig(level=logging.INFO)


MAX_READ_BYTES = 4096


def get_url(request: str) -> Optional[str]:
    match = re.search("(?<=GET ).+(?= HTTP/1.1.+)", request)
    if not match:
        return match
    return match.group(0)


def get_host_port_path(
    request: bytearray,
) -> Tuple[Optional[str], Optional[int], Optional[str]]:
    url = get_url(request.decode("utf-8"))
    if not url:
        return None, None, None
    parsed_url = urlparse(url)
    return parsed_url.hostname, parsed_url.port or 80, parsed_url.path or "/"


@asynccontextmanager
async def writer(tx: asyncio.StreamWriter) -> asyncio.StreamWriter:
    try:
        yield tx
    finally:
        logging.info("closing")
        tx.close()
        await tx.wait_closed()


def managed_writer(handler_coro):
    @wraps(handler_coro)
    async def handler_with_managed_writer(
        rx: asyncio.StreamReader, tx: asyncio.StreamWriter, *args, **kwargs,
    ):
        async with writer(tx) as tx_managed:
            return await handler_coro(rx, tx_managed, *args, **kwargs)

    return handler_with_managed_writer


async def read_all(
    rx: asyncio.StreamReader, max_read_bytes: int = MAX_READ_BYTES
) -> bytearray:
    full_data = b""
    while True:
        data = await rx.read(max_read_bytes)
        logging.info("Data length: {} bytes".format(len(data)))
        logging.info("Data:\n{}".format(data))
        if not data:
            return data
        full_data += data
        if 0 < len(data) <= max_read_bytes:
            return full_data


async def write_all(tx: asyncio.StreamWriter, data: bytearray) -> None:
    logging.info("Writing: {} bytes".format(len(data)))
    tx.write(data)
    await tx.drain()


@managed_writer
async def handle_request(
    rx_loc: asyncio.StreamReader, tx_loc: asyncio.StreamWriter,
) -> None:
    while True:
        request_bytes = await read_all(rx_loc)
        if not request_bytes:
            logging.info("no data from the client")
            return
        host, port, path = get_host_port_path(request_bytes)
        if not host:
            logging.info("no host in the url")
            return
        logging.info("{} {} {}".format(host, port, path))
        rx_ext, tx_ext = await asyncio.open_connection(host=host, port=port)
        await write_all(tx_ext, request_bytes)
        response_bytes = await read_all(rx_ext)
        tx_ext.close()
        await tx_ext.wait_closed()
        if not response_bytes:
            logging.info("no data from the external server")
            return
        await write_all(tx_loc, response_bytes)


@managed_writer
async def handle_request_keep_connection(
    rx_loc: asyncio.StreamReader, tx_loc: asyncio.StreamWriter,
) -> None:
    request_init_bytes = await read_all(rx_loc)
    if not request_init_bytes:
        logging.info("no data from the client")
        return
    host, port, path = get_host_port_path(request_init_bytes)
    if not host:
        logging.info("no host in the url")
        return
    logging.info("{} {} {}".format(host, port, path))
    await write_all(tx_loc, b"HTTP/1.1 200 OK")
    rx_ext, tx_ext = await asyncio.open_connection(host=host, port=port)

    @managed_writer
    async def run_proxy(
        rx_ext: asyncio.StreamReader, tx_ext: asyncio.StreamWriter,
    ) -> None:
        while True:
            request_bytes = await read_all(rx_loc)
            if not request_bytes:
                logging.info("no data from the client")
                return
            await write_all(tx_ext, request_bytes)
            response_bytes = await read_all(rx_ext)
            if not response_bytes:
                logging.info("no data from the external server")
                return
            await write_all(tx_loc, response_bytes)

    await run_proxy(rx_ext, tx_ext)


async def server():
    serv = await asyncio.start_server(handle_request, "localhost", 9090)
    async with serv:
        await serv.serve_forever()


if __name__ == "__main__":
    asyncio.run(server())
