from . import enums, tools


class MetadataAPIWrapper:
    def __init__(
        self, username: str, password: str, language: enums.Language = enums.Language.GERMAN
    ):
        """Create a new HelloWorldAPIWrapper method wrapper

        :param username: The username which was assigned during the creation of an account (
            length: 10 characters)
        :type username: str
        :param password: The password for the username (length: 10-20 characters)
        :type password: str
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
        self._username = username
        self._password = password
        self._language = language
        self._service_url = "/metadata"
        self._base_parameter = {
            "username": self._username,
            "password": self._password,
            "language": self._language.value,
        }

    async def cube(
        self, object_name: str, storage_location: enums.ObjectStorage = enums.ObjectStorage.ALL
    ) -> dict:
        """
        Get metadata about a data cube

        :param object_name: The object's identification code
        :type object_name: str
        :param storage_location: The storage location of the object, defaults to
        :py:enum:mem:`enums.ObjectStorage.ALL`
        :type storage_location: enums.ObjectStorage
        :return: The response from the database
        :rtype: dict
        """
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        # Build the query parameter
        query_parameter = self._base_parameter | {
            "name": object_name,
            "area": storage_location.value,
        }
        # Build the query path
        query_path = self._service_url + "/cube"
        # Get the response
        return await tools.get_database_response(query_path, query_parameter)

    async def statistic(
        self, object_name: str, storage_location: enums.ObjectStorage = enums.ObjectStorage.ALL
    ) -> dict:
        """
        Get metadata about a statistic

        :param object_name: The object's identification code
        :type object_name: str
        :param storage_location: The storage location of the object, defaults to
        :py:enum:mem:`enums.ObjectStorage.ALL`
        :type storage_location: enums.ObjectStorage
        :return: The response from the database
        :rtype: dict
        """
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        # Build the query parameter
        query_parameter = self._base_parameter | {
            "name": object_name,
            "area": storage_location.value,
        }
        # Build the query path
        query_path = self._service_url + "/statistic"
        # Get the response
        return await tools.get_database_response(query_path, query_parameter)

    async def table(
        self, object_name: str, storage_location: enums.ObjectStorage = enums.ObjectStorage.ALL
    ) -> dict:
        """
        Get metadata about a table

        :param object_name: The object's identification code
        :type object_name: str
        :param storage_location: The storage location of the object, defaults to
        :py:enum:mem:`enums.ObjectStorage.ALL`
        :type storage_location: enums.ObjectStorage
        :return: The response from the database
        :rtype: dict
        """
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        # Build the query parameter
        query_parameter = self._base_parameter | {
            "name": object_name,
            "area": storage_location.value,
        }
        # Build the query path
        query_path = self._service_url + "/table"
        # Get the response
        return await tools.get_database_response(query_path, query_parameter)

    async def timeseries(
        self, object_name: str, storage_location: enums.ObjectStorage = enums.ObjectStorage.ALL
    ) -> dict:
        """
        Get metadata about a table

        :param object_name: The object's identification code
        :type object_name: str
        :param storage_location: The storage location of the object, defaults to
        :py:enum:mem:`enums.ObjectStorage.ALL`
        :type storage_location: enums.ObjectStorage
        :return: The response from the database
        :rtype: dict
        """
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        # Build the query parameter
        query_parameter = self._base_parameter | {
            "name": object_name,
            "area": storage_location.value,
        }
        # Build the query path
        query_path = self._service_url + "/timeseries"
        # Get the response
        return await tools.get_database_response(query_path, query_parameter)

    async def value(
        self, object_name: str, storage_location: enums.ObjectStorage = enums.ObjectStorage.ALL
    ) -> dict:
        """
        Get metadata about a table

        :param object_name: The object's identification code
        :type object_name: str
        :param storage_location: The storage location of the object, defaults to
        :py:enum:mem:`enums.ObjectStorage.ALL`
        :type storage_location: enums.ObjectStorage
        :return: The response from the database
        :rtype: dict
        """
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        # Build the query parameter
        query_parameter = self._base_parameter | {
            "name": object_name,
            "area": storage_location.value,
        }
        # Build the query path
        query_path = self._service_url + "/value"
        # Get the response
        return await tools.get_database_response(query_path, query_parameter)

    async def variable(
        self, object_name: str, storage_location: enums.ObjectStorage = enums.ObjectStorage.ALL
    ) -> dict:
        """
        Get metadata about a table

        :param object_name: The object's identification code
        :type object_name: str
        :param storage_location: The storage location of the object, defaults to
        :py:enum:mem:`enums.ObjectStorage.ALL`
        :type storage_location: enums.ObjectStorage
        :return: The response from the database
        :rtype: dict
        """
        if not object_name:
            raise ValueError("The object_name is a required parameter")
        if not (1 <= len(object_name.strip()) <= 15):
            raise ValueError("The object_name may only contain between 1 and 15 characters")
        # Build the query parameter
        query_parameter = self._base_parameter | {
            "name": object_name,
            "area": storage_location.value,
        }
        # Build the query path
        query_path = self._service_url + "/variable"
        # Get the response
        return await tools.get_database_response(query_path, query_parameter)
