from . import enums, tools


class ProfileAPIWrapper:
    def __init__(
        self, username: str, password: str, language: enums.Language = enums.Language.GERMAN
    ):
        """Create a new HelloWorldAPIWrapper method wrapper

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
        self._username = username
        self._password = password
        self._language = language
        self._service_url = "/profile"
        self._base_parameter = {
            "username": self._username,
            "password": self._password,
            "language": self._language.value,
        }

    async def password(self, new_password: str):
        """
        Change the password of the current user.

        After invoking this function you need to recreate your wrapper

        :param new_password: The new password
        :type new_password: str
        :return: The response from the server
        :rtype: dict
        """
        if not (10 <= len(new_password) <= 20):
            raise ValueError(
                "The new password has the following length constraints: min. 10 "
                "chars, max. 20 chars"
            )
        query_parameter = self._base_parameter | {"new": new_password, "repeat": new_password}
        query_path = self._service_url + "/password"
        return await tools.get_database_response(query_path, query_parameter)

    async def remove_result(
        self, object_name: str, storage_location: enums.ObjectStorage = enums.ObjectStorage.ALL
    ):
        """
        Remove a result table from the specified area

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
        query_parameters = self._base_parameter | {
            "name": object_name,
            "area": storage_location.value,
        }
        query_path = self._service_url + "removeResult"
        return await tools.get_database_response(query_path, query_parameters)
