from . import enums
from . import tools


class HelloWorldAPIWrapper:
    """All methods from the HelloWorldAPIWrapper section of the API documentation"""

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
