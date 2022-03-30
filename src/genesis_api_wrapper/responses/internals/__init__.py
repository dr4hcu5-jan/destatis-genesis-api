"""A package containing all 2nd and lower level response models"""
from pydantic import Field, Extra

from ...enums import GENESISLanguage
from ...models import BaseModel


class ServiceIdent(BaseModel):
    """
    The identification information about the called service and the method of that service
    """

    service: str = Field(default=..., alias="Service", title="Name of the Service")
    """
    Name of the Service
    
    This field represents the called service from the database    
    """

    method: str = Field(default=..., alias="Method", title="Method of Service")
    """
    Method of the called service
    """


class Status(BaseModel):
    """
    A part of every request which contains a status message
    """

    code: int = Field(
        default=...,
        alias="Code",
        title="Status code of the request",
        description="Identification number of the error",
    )
    """
    GENESIS Internal status code of the request
    
    Identification of an error which may have occurred. If no error occurred the field is set to zero (0) 
    """

    content: str = Field(default=..., alias="Content", title="Content")
    """
    GENESIS Error information
    
    Textual description of an error. If no error occurred this field is set to "erfolgreich"
    """

    type: str = Field(default=..., alias="Type", title="Content Type")
    """
    GENESIS Information Type
    
    Type of the information present in this request in reference to the error
    """


class RequestParameter(BaseModel):
    """
    Parameters used by the called service to process the request
    """

    language: GENESISLanguage = Field(default=..., alias="language")
    """
    Search language
    
    The language in which the documents are available
    """

    class Config:
        """Configuration of the Request Parameters"""

        extra = Extra.allow
        """Allow additional fields to be assigned """
