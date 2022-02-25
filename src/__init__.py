"""Wrapper for the JSON API of the DESTATIS GENESIS database"""
import logging

import aiohttp
from pydantic import SecretStr

from enums import GENESISLanguage, GENESISCategory
from responses import *

# Create a logger for the whole module
MODULE_LOGGER = logging.getLogger('DESTATIS-API')
"""The logger which is used in this module"""


class GENESISWrapper:
    """
    The wrapper for the API access
    """

    def __init__(
            self,
            username: str,
            password: str,
            language: GENESISLanguage = GENESISLanguage.ENGLISH
    ):
        """Create a new GENESIS database wrapper

        :param username: The username which was assigned during the creation of an account (length: 10 characters)
        :type username: str
        :param password: The password for the username (length: 10-20 characters)
        :type password: SecretStr
        :param language: The language which should be used in the response bodies, defaults to English
        :type language: GENESISLanguage
        """
        # Check if the username consists of 10 characters
        if len(username) != 10:
            raise ValueError("The username is not 10 characters long.")
        # Check if the password's length is between 10 and 20 characters
        if not (10 <= len(password) <= 20):
            raise ValueError("The password is not between 10 and 20 characters long")
        # Since all values passed the check save the username and password to the wrapper, but keep them private
        self.__username = username
        self.__password = SecretStr(password)
        self.__language = language
        self.__base_url = 'https://www-genesis.destatis.de/genesisWS/rest/2020'

    async def whoami(self) -> GENESISWhoAmIResponse:
        """Execute the whoami method of the GENESIS API"""
        async with aiohttp.ClientSession() as http_session:
            _url = self.__base_url + '/helloworld/whoami'
            async with http_session.get(_url) as response:
                data = await response.json()
                return GENESISWhoAmIResponse.parse_obj(data)

    async def login_check(self) -> GENESISLoginCheckResponse:
        async with aiohttp.ClientSession() as http_session:
            _url = self.__base_url + '/helloworld/logincheck'
            _body = {
                'username': self.__username,
                'password': self.__password.get_secret_value(),
                'language': self.__language.value
            }
            async with http_session.get(_url, params=_body) as response:
                data = await response.text()
                return GENESISLoginCheckResponse.parse_raw(data)
