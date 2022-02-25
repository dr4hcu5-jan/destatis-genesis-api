"""Responses which are received from the GENESIS database"""

from pydantic import BaseModel, Field


class __BaseGENESISResponse(BaseModel):
    """
    A Basic Class used for all responses from the GENESIS database which presets some configuration variables
    """

    class Config:
        """Configuration which is inherited into every other Response"""

        allow_population_by_field_name = True
        """Allow the population of the fields by their names and aliases"""


class GENESISWhoAmIResponse(__BaseGENESISResponse):
    """
    The contents of the response after requesting the "whoami" method on the api
    """

    user_agent: str = Field(
        default=...,
        alias='User-Agent',
        description='The user-agent header present in the request which was send'
    )

    user_ip: str = Field(
        default=...,
        alias='User-IP',
        description='The IP address from which the call was made'
    )


class GENESISLoginCheckResponse(__BaseGENESISResponse):
    """The contents of the response after requesting the "logincheck" method on the api"""

    username: str = Field(
        default=...,
        alias='Username'
    )

    status: str = Field(
        default=...,
        alias='Status'
    )
