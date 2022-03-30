"""Wrapper for the JSON API of the DESTATIS GENESIS database"""
from . import enums, find, catalogue, data, hello_world, metadata, profile


class APIWrapper:
    def __init__(
        self, username: str, password: str, language: enums.Language = enums.Language.GERMAN
    ):
        """
        A wrapper for the GENESIS database hosted by the Federal Statistical Office of Germany

        Included Wrappers:
          - :class:`hello_world.HelloWorldAPIWrapper` - A wrapper containing methods for testing the
            access to the database
          - :class:`find.FindAPIWrapper` - A wrapper containing methods for finding objects in the
            database
          - :class:`catalogue.CatalogueAPIWrapper` - A wrapper containing functions for listing the
            different object types available in the database
          - :class:`data.DataAPIWrapper` - A wrapper containing functions for downloading data from
            the database in different formats
          - :class:`metadata.MetadataAPIWrapper` - A wrapper containing functions for receiving
            metadata of some object types
          - :class:`profile.ProfileAPIWrapper` - A wrapper containing functions for modifying the
            profile which is used to access the database

        Notice: This wrapper and all partial wrappers are working asynchronously. Therefore,
        your need to use :mod:`asyncio` while using the wrapper in synchronous calls

        :param username: The username which will be used for authenticating at the database. Due
            to constraints of the database the username needs to be exactly 10 characters long and
            may not contain any whitespaces
        :type username: str
        :param password: The password which will be used for authenticating at the database. Due
            to constraints of the database the password needs to be at least 10 characters long,
            may not exceed 20 characters and may not contain any whitespaces
        :type password: str
        :param language: The language in which the responses are returned by the database.
            :py:enum:mem:`~enums.Language.GERMAN` has the most compatibility with the database
            since most of the tables are on German. Therefore, this parameter defaults to
            :py:enum:mem:`~enums.Language.GERMAN`
        :type language: enums.Language
        :raise ValueError: The username or the password did not match the constraints stated in
            their description.
        """
        if " " in username:
            raise ValueError("The username may not contain any whitespaces")
        if len(username) != 10:
            raise ValueError("The username may only be 10 characters long")
        if " " in password:
            raise ValueError("The password may not contain any whitespaces")
        if len(password) < 10:
            raise ValueError(
                f"The password may not be shorter than 10 characters. Current "
                f"length: {len(password)}"
            )
        if len(password) > 20:
            raise ValueError(
                f"The password may not be longer that 20 characters. Current "
                f"length: {len(password)}"
            )
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
        """
        Methods for testing the access to the database and for validating the credentials
        """

        self.find: find.FindAPIWrapper = find.FindAPIWrapper(username, password, language)
        """
        Methods for searching objects in the database
        """

        self.catalogue: catalogue.CatalogueAPIWrapper = catalogue.CatalogueAPIWrapper(
            username, password, language
        )
        """
        Methods for listing objects of different types which are stored in the database
        
        Using the following functions require premium access to the database:
            - :meth:`~catalogue.CatalogueAPIWrapper.cubes`
            - :meth:`~catalogue.CatalogueAPIWrapper.cubes2statistic`
            - :meth:`~catalogue.CatalogueAPIWrapper.cubes2variable`
            
        """

        self.data: data.DataAPIWrapper = data.DataAPIWrapper(username, password, language)
        """
        Methods for downloading objects from the database in different formats and styles
        
        Using the following functions require premium access to the database:
            - :meth:`~data.DataAPIWrapper.cube`
            - :meth:`~data.DataAPIWrapper.cube_file`
        """

        self.metadata: metadata.MetadataAPIWrapper = metadata.MetadataAPIWrapper(
            username, password, language
        )
        """
        Methods for accessing metadata about some object types stored in the database
        
        Using the following functions require premium access to the database:
            - :meth:`~metadata.MetadataAPIWrapper.cube`
        """

        self.profile: profile.ProfileAPIWrapper = profile.ProfileAPIWrapper(
            username, password, language
        )
        """
        Methods for changing the accounts password and removing result tables from the account
        """
