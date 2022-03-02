"""Wrapper for the JSON API of the DESTATIS GENESIS database"""
import datetime
import logging
from datetime import timedelta

from pydantic import SecretStr

import tools
from enums import GENESISLanguage, GENESISCategory, GENESISJobType, GENESISJobCriteria, \
    GENESISObjectType
from responses import *

# Create a logger for the whole module
logger = logging.getLogger('DESTATIS-GENESIS')
"""The logger which is used in this module"""


class GENESISWrapper:
    """
    The wrapper for the API access
    """

    def __init__(
            self,
            username: str,
            password: str,
            language: GENESISLanguage = GENESISLanguage.GERMAN
    ):
        """Create a new GENESIS database wrapper

        :param username: The username which was assigned during the creation of an account(
            length: 10 characters)
        :type username: str
        :param password: The password for the username (length: 10-20 characters)
        :type password: SecretStr
        :param language: The language which should be used in the response bodies, defaults to
            German
        :type language: GENESISLanguage
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
        self.__password = SecretStr(password)
        self.__language = language
        self.__base_parameter = {
            'username': self.__username,
            'password': self.__password.get_secret_value(),
            'language': self.__language.value
        }
        self.hello_world: GENESISWrapper.HelloWorld = self.HelloWorld(username, password, language)
        """Methods in the `Hello World` part of the official API documentation"""
        self.find: GENESISWrapper.Find = self.Find(username, password, language)
        """Methods in the `Find` part of the official API documentation"""
        self.catalogue: GENESISWrapper.Catalogue = self.Catalogue(username, password, language)
        """Methods in the `Catalogue` part of the official API documentation"""
    
    class HelloWorld:
        """All methods from the HelloWorld section of the API documentation"""

        def __init__(
                self,
                username: str,
                password: str,
                language: GENESISLanguage = GENESISLanguage.GERMAN
        ):
            """Create a new HelloWorld method wrapper

            :param username: The username which was assigned during the creation of an account (
            length: 10 characters)
            :type username: str
            :param password: The password for the username (length: 10-20 characters)
            :type password: SecretStr
            :param language: The language which should be used in the response bodies, defaults to
            German
            :type language: GENESISLanguage
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
            self.__password = SecretStr(password)
            self.__language = language
            self.__base_parameter = {
                'username': self.__username,
                'password': self.__password.get_secret_value(),
                'language': self.__language.value
            }
        
        @staticmethod
        async def who_am_i() -> HelloWorld.WhoAmIResponse:
            """Get information about the client data transmitted to the GENESIS database
            
            :return: A Response containing the IP Address and the User-Agent for the request that
            has
                been executed
            :rtype: WhoAmIResponse
            """
            return await tools.get_parsed_response('/helloworld/whoami', None,
                                                   HelloWorld.WhoAmIResponse)
    
        async def login_check(self) -> HelloWorld.LoginCheckResponse:
            """Check the login data which were supplied during the creation of the wrapper
            
            :return: The response from the server containing the success or failure of the reqeust
            :rtype: LoginCheckResponse
            """
            return await tools.get_parsed_response(
                '/helloworld/logincheck',
                self.__base_parameter,
                HelloWorld.LoginCheckResponse
            )
    
    class Find:
    
        def __init__(
                self,
                username: str,
                password: str,
                language: GENESISLanguage = GENESISLanguage.GERMAN
        ):
            """Create a new Find section method wrapper

            :param username: The username which was assigned during the creation of an account (
            length: 10 characters)
            :type username: str
            :param password: The password for the username (length: 10-20 characters)
            :type password: SecretStr
            :param language: The language which should be used in the response bodies, defaults to
            German
            :type language: GENESISLanguage
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
            self.__password = SecretStr(password)
            self.__language = language
            self.__base_parameter = {
                'username': self.__username,
                'password': self.__password.get_secret_value(),
                'language': self.__language.value
            }
    
        async def find(
                self,
                search_term: str,
                category: GENESISCategory = GENESISCategory.ALL,
                results_per_category: int = 100
        ) -> Find.FindResult:
            """Get a list of objects in the specified category which match the search term
            
            :param search_term: Term for which the search is executed
            :param category: The category in which the search is executed
            :param results_per_category: Number of results per category
            :return: A response containing the results of the search
            """
            _params = self.__base_parameter | {
                'term':       search_term,
                'category':   category.value,
                'pagelength': str(results_per_category)
            }
            return await tools.get_parsed_response('/find/find', _params, Find.FindResult)
    
    class Catalogue:
    
        def __init__(
                self,
                username: str,
                password: str,
                language: GENESISLanguage = GENESISLanguage.GERMAN
        ):
            """Create a new Find section method wrapper

            :param username: The username which was assigned during the creation of an account (
            length: 10 characters)
            :type username: str
            :param password: The password for the username (length: 10-20 characters)
            :type password: SecretStr
            :param language: The language which should be used in the response bodies, defaults to
            German
            :type language: GENESISLanguage
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
            self.__password = SecretStr(password)
            self.__language = language
            self.__service = '/catalogue'
            self.__base_parameter = {
                'username': self.__username,
                'password': self.__password.get_secret_value(),
                'language': self.__language.value
            }
            
        async def cubes(
                self,
                selection: str,
                results: int = 100
        ) -> Catalogue.CubeResponse:
            """Get a list of data cubes matching the selector (PREMIUM ACCOUNTS ONLY)
            
            :param selection: The code of the data cube. You may use a star (*) to allow wild
            carding
            :param results: The maximum items which are received from the database
            :return: A list of information about the found data cubes
            """
            _parameters = self.__base_parameter | {
                'selection': selection,
                'pagelength': str(results)
            }
            _url = self.__service + '/cubes'
            return await tools.get_parsed_response(_url, _parameters, Catalogue.CubeResponse)
        
        async def cubes_to_statistic(
                self,
                statistic_name: constr(min_length=1, max_length=6),
                cube_code: constr(min_length=1, max_length=10),
                results: int = 100
        ) -> Catalogue.CubeResponse:
            """Get a list of data cubes of a statistic matching the selector (PREMIUM ACCOUNTS ONLY)
            
            :param statistic_name: The name of the statistic that shall be used
            :param cube_code: The code of the data cube in this statistic, star based wild-carding
                is allowed
            :param results: The number of maximum results that should be pulled
            :return: A list of information about the data cubes
            """
            _parameters = self.__base_parameter | {
                'name': statistic_name,
                'selection':  cube_code,
                'pagelength': str(results)
            }
            _url = self.__service + '/cubes2statistic'
            return await tools.get_parsed_response(_url, _parameters, Catalogue.CubeResponse)
    
        async def cubes_to_variable(
                self,
                variable_name: constr(min_length=1, max_length=6),
                cube_code: constr(min_length=1, max_length=10),
                results: int = 100
        ) -> Catalogue.CubeResponse:
            """Get a list of data cubes related to the specified variable
            
            :param variable_name: The name of the variable, (max. 6 character)
            :param cube_code: The code of a cube which is related to the variable, stars (*) may be
                used for wild carding
            :param results: Number of results which are retrieved
            :return: A list of the data cubes which are related to the variable
            """
            _parameters = self.__base_parameter | {
                'name': variable_name,
                'selection': cube_code,
                'pagelength': results
            }
            _url = self.__service + '/cubes2variable'
            return await tools.get_parsed_response(
                _url,
                _parameters,
                Catalogue.CubeResponse
            )
        
        async def jobs(
                self,
                selector: str,
                search_by: GENESISJobCriteria,
                sort_by: GENESISJobCriteria,
                job_type: GENESISJobType = GENESISJobType.ALL,
                results: int = 100
        ) -> Catalogue.JobResponse:
            """Get a list of jobs which were created
            
            :param selector: Filter for the jobs to be displayed. (1-50 characters, stars (*)
                allowed for wildcarding)
            :param search_by: The criteria on which the selector is applied to
            :param sort_by: The criteria by which the result shall be listed
            :param job_type: The type of job which is to be returned
            :param results: The number of results that shall be returned
            :return:
            """
            if not (1 <= len(selector) <= 50):
                raise ValueError('The length of the selector needs to be between 1 and 50 ('
                                 'inclusive)')
            if None in [search_by, sort_by]:
                raise ValueError('All parameter without a default value need to be set')
            _params = self.__base_parameter | {
                'selection': selector,
                'searchcriterion': search_by.value,
                'sortcriterion': sort_by.value,
                'type': job_type.value,
                'area': 'all'
            }
            _url = self.__service + '/jobs'
            return await tools.get_parsed_response(_url, _params, Catalogue.JobResponse)
        
        async def modified_data(
                self,
                selector: Optional[str] = None,
                object_type: GENESISObjectType = GENESISObjectType.ALL,
                updated_after: Optional[date] = None,
                results: int = 100
        ) -> Catalogue.ModifiedDataResponse:
            """Get a list of modified objects
            
            :param selector: Filter for the objects to be displayed. (1-15 characters, stars (*)
                allowed for wildcarding)
            :type selector: str
            :param object_type: The type of object that shall be returned
            :type object_type: GENESISObjectType
            :param updated_after: The date after which the objects needed to be changed to be
                returned, defaults to one week (7 days)
            :type updated_after: date
            :param results: The number of results that should be returned
            """
            # Check the parameters for consistency
            if (selector is not None) and (not (1 <= len(selector) <= 15)):
                raise ValueError("The selector's length needs to be between 1 and 15 (inclusive)")
            if (updated_after is not None) and not (updated_after < date.today()):
                print(updated_after)
                print(date.today())
                raise ValueError("The specified date may not be today or in the future")
            if not (0 < results <= 2500):
                raise ValueError('The number of results need to be between 1 and 2500')
            # Build the query parameters
            _param = self.__base_parameter | {
                'selection': '' if selector is None else selector,
                'type': GENESISObjectType.ALL.value if object_type is None else object_type.value,
                'date': updated_after.strftime('%d.%m.%Y') if updated_after is not None else None,
                'pagelength': results
            }
            _url = self.__service + '/modifieddata'
            return await tools.get_parsed_response(_url, _param, Catalogue.ModifiedDataResponse)
            