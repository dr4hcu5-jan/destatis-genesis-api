from . import enums, tools


class HelloWorldAPIWrapper:
    """All methods from the HelloWorldAPIWrapper section of the API documentation"""

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
        self._service_url = "/helloworld"
        self._base_parameter = {
            "username": self._username,
            "password": self._password,
            "language": self._language.value,
        }

    @staticmethod
    async def who_am_i() -> dict:
        """Get information about the client data transmitted to the GENESIS database

        :return: A Response containing the IP Address and the User-Agent for the request that
            has been executed
        :rtype: dict
        """
        return await tools.get_database_response("/helloworld/whoami", {})

    async def login_check(self) -> dict:
        """Check the login data which were supplied during the creation of the wrapper

        :return: The response from the server containing the success or failure of the reqeust
        :rtype: dict
        """
        return await tools.get_database_response("/helloworld/logincheck", self._base_parameter)
