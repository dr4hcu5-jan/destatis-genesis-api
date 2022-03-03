"""A collection of tools which are used and needed multiple times in this project"""
import asyncio
import logging
import time
from typing import TypeVar, Union, Type

import aiohttp
from pydantic import ValidationError

from exceptions import GENESISPermissionError, GENESISInternalServerError
from responses import *

logger = logging.getLogger('DESTATIS-GENESIS')

ResponseType = Type[
    Union[
        HelloWorld.WhoAmIResponse, HelloWorld.LoginCheckResponse,
        Find.FindResult,
        Catalogue.CubeResponse, Catalogue.JobResponse, Catalogue.ModifiedDataResponse
    ]
]


async def is_host_available(
        host: str,
        port: int,
        timeout: int
) -> bool:
    """Check if the specified host is reachable on the specified port

    :param host: The hostname or ip address which shall be checked
    :param port: The port which shall be checked
    :param timeout: Max. duration of the check
    :return: A boolean indicating the status
    """
    _end_time = time.time() + timeout
    while time.time() < timeout:
        try:
            # Try to open a connection to the specified host and port and wait a maximum time of five seconds
            _s_reader, _s_writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=5)
            # Close the stream writer again
            _s_writer.close()
            # Wait until the writer is closed
            await _s_writer.wait_closed()
            return True
        except:
            # Since the connection could not be opened wait 5 seconds before trying again
            await asyncio.sleep(5)
    return False


async def get_raw_json_response(
        path: str,
        parameters: Optional[dict],
) -> dict:
    """Request a resource from the GENESIS API from the specified path

    :param path: The path that shall be queried
    :param parameters: The optional parameters for this request
    :return:
    """
    for key, value in dict(parameters).items():
        if value is None:
            del parameters[key]
    async with aiohttp.ClientSession() as http_session:
        _url = 'https://www-genesis.destatis.de/genesisWS/rest/2020' + path
        async with http_session.get(_url, params=parameters) as response:
            # Check if the response is a 200 response
            if response.status == 200:
                data = await response.json()
                return data
            elif response.status == 401:
                raise GENESISPermissionError
            elif response.status == 500:
                raise GENESISInternalServerError


async def get_parsed_response(
        path: str,
        parameters: Optional[dict],
        r: ResponseType
) -> type(ResponseType):
    """Request a resource from the GENESIS API from the specified path
    
    :param path: The path that shall be queried
    :param parameters: The optional parameters for this request
    :param r: The PydanticModel into which the response is parsed
    :return:
    """
    try:
        return r.parse_obj(await get_raw_json_response(path, parameters))
    except ValidationError as error:
        logger.error('Error during parsing the response received from the database. '
                            'Printing response into terminal...')
        print(await get_raw_json_response(path, parameters))
