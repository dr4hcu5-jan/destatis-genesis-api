import typing

from . import enums, tools


class ProfileAPIWrapper:
    
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
            raise ValueError('The new password has the following length constraints: min. 10 '
                             'chars, max. 20 chars')
        query_parameter = self._base_parameter | {
            'new': new_password,
            'repeat': new_password
        }
        query_path = self._service_url + '/password'
        return await tools.get_database_response(query_path, query_parameter)
    
    def remove_result(
            self,
            object_name: str,
            storage_location: enums.ObjectStorage = enums.ObjectStorage.ALL
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
            'name': object_name,
            'area': storage_location.value
        }
        query_path = self._service_url + 'removeResult'
        return await tools.get_database_response(query_path, query_parameters)
