"""Wrapper for the JSON API of the DESTATIS GENESIS database"""
import logging

from . import tools, enums, find, catalogue, data, hello_world

# Create a logger for the whole module
logger = logging.getLogger("genesis_api_wrapper")
"""The logger which is used in this module"""


class APIWrapper:
    """
    An asynchronous Wrapper for the GENESIS API
    """

    def __init__(
        self, username: str, password: str, language: enums.Language = enums.Language.GERMAN
    ):
        """Create a new GENESIS database wrapper

        :param username: The username which was assigned during the creation of an account(
            length: 10 characters)
        :type username: str
        :param password: The password for the username (length: 10-20 characters)
        :type password: SecretStr
        :param language: The language which should be used in the response bodies, defaults to
            German
        :type language: Language
        """
        # Check if the username consists of 10 characters
        if len(username) != 10:
            raise ValueError("The username is not 10 characters long.")
        # Check if the password's length is between 10 and 20 characters
        if not (10 <= len(password) <= 20):
            raise ValueError("The password is not between 10 and 20 characters long")
        # Since all values passed the check save the username and password to the wrapper,
        # but keep them private
        self.__username = username
        self.__password = password
        self.__language = language
        self.__base_parameter = {
            "username": self.__username,
            "password": self.__password,
            "language": self.__language.value,
        }
        self.hello_world: hello_world.HelloWorldAPIWrapper = hello_world.HelloWorldAPIWrapper(
            username, password, language
        )
        """Methods in the `Hello World` part of the official API documentation"""
        self.find: find.FindAPIWrapper = find.FindAPIWrapper(username, password)
        """Methods in the `FindAPIWrapper` part of the official API documentation"""
        self.catalogue: catalogue.CatalogueAPIWrapper = catalogue.CatalogueAPIWrapper(
            username, password
        )
        """Methods in the `Catalogue` part of the official API documentation"""
        self.data: data.DataAPIWrapper = data.DataAPIWrapper(username, password)
        """Methods in the `DataAPIWrapper` part of the official API documentation"""
