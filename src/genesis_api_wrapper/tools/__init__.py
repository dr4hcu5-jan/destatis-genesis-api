"""A collection of tools which are used and needed multiple times in this project"""
import asyncio
import logging
import mimetypes
import secrets
import time
import tempfile
from os import PathLike
from pathlib import Path
from typing import TypeVar, Union, Type, Optional

import aiohttp

from ..exceptions import GENESISPermissionError, GENESISInternalServerError

logger = logging.getLogger("DESTATIS-GENESIS")

TEMP_DIR = tempfile.mkdtemp(suffix="genesis-wrapper")


async def is_host_available(host: str, port: int, timeout: int) -> bool:
    """Check if the specified host is reachable on the specified port

    :param host: The hostname or ip address which shall be checked
    :param port: The port which shall be checked
    :param timeout: Max. duration of the check
    :return: A boolean indicating the status
    """
    _end_time = time.time() + timeout
    while time.time() < timeout:
        try:
            # Try to open a connection to the specified host and port and wait a maximum time of
            # five seconds
            _s_reader, _s_writer = await asyncio.wait_for(
                asyncio.open_connection(host, port), timeout=5
            )
            # Close the stream writer again
            _s_writer.close()
            # Wait until the writer is closed
            await _s_writer.wait_closed()
            return True
        except:
            # Since the connection could not be opened wait 5 seconds before trying again
            await asyncio.sleep(5)
    return False


async def get_database_response(
    query_path: str, query_parameters: Optional[dict]
) -> Union[dict, PathLike]:
    """Download an image from the database

    This will try to download an image from the specified method with the specified parameters.

    If the response does not contain a valid content type for an image the response will be
    returned as json (if the response is json parseable). If the response is not parseable the
    response will be written to a file which has the file extension set by the content type

    :param query_path: The path that shall be queries
    :type query_path: str
    :param query_parameters: The parameters that shall be used for the query
    :type query_parameters: dict
    :return: The path to the image
    """
    # Check if a query path has been set
    if not query_path:
        raise ValueError("The query_path is a required parameter")
    # Cleanup possible None values from the request
    for key, value in dict(query_parameters).items():
        if value is None:
            del query_parameters[key]
    # Create the url which will be called
    url = "https://www-genesis.destatis.de/genesisWS/rest/2020" + query_path
    # Start downloading the image
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=query_parameters) as response:
            # Check if any error occurred during the request
            if response.status == 401:
                raise GENESISPermissionError("This account is not allowed to access this service")
            if 500 <= response.status <= 599:
                raise GENESISInternalServerError(
                    "An error occurred on the server side. Please " "try again"
                )
            # Check if the content type indicates a json response
            if response.content_type == "application/json":
                return await response.json()
            else:
                _file_ending = mimetypes.guess_extension(response.content_type)
                _file_name = secrets.token_urlsafe(nbytes=128)
                _file_path = f"{TEMP_DIR}/{_file_name}{_file_ending}"
                with open(_file_path, "wb") as file:
                    async for _file_chunk in response.content.iter_chunked(128):
                        file.write(_file_chunk)
                    file.close()
                return Path(_file_path)
