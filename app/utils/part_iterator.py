from aiohttp import StreamReader


async def reader_iterator(reader: StreamReader, chunk_size: int = 5 * 1024 ** 2):
    while not reader.at_eof():
        chunk = b''
        while not reader.at_eof() and len(chunk) < chunk_size:
            chunk += await reader.read(chunk_size)
        yield chunk
