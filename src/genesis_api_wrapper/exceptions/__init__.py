class GENESISPermissionError(Exception):
    """
    Exceptions raised if the account may not access the specified service and method
    """

    pass


class GENESISInternalServerError(Exception):
    """
    Exception raised if the server occurred an internal error
    """
