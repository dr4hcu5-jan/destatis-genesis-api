# GENESIS database API wrapper
[![CodeQL](https://github.com/j-suchard/destatis-genesis-api/actions/workflows/code-analysis.yaml/badge.svg)](https://github.com/j-suchard/destatis-genesis-api/actions/workflows/code-analysis.yaml)
[![OSSAR](https://github.com/j-suchard/destatis-genesis-api/actions/workflows/ossar.yaml/badge.svg)](https://github.com/j-suchard/destatis-genesis-api/actions/workflows/ossar.yaml)
[![Pylint](https://github.com/j-suchard/destatis-genesis-api/actions/workflows/pylint.yaml/badge.svg?branch=main)](https://github.com/j-suchard/destatis-genesis-api/actions/workflows/pylint.yaml)

This library offers a Python implementation of the RESTful API the GENESIS databases hosted by 
the DESTATIS (Federal Statistical Office of Germany).

## Credentials
To successfully use the GENESIS database instance of the DESTATIS you will need to create some 
credentials at the [Registration Page](https://www-genesis.destatis.de/genesis/online?Menu=Registrierung#abreadcrumb)

> *Note*: Some services are only accessible for premium access users. Using methods of those 
> services will result in an Error

## Usage
### General

This wrapper is implemented in an asynchronous way. Meaning you will need to await your calls to 
the wrapper. If you are using the wrapper in a synchronous application you will need to work 
with `asyncio` and their event loops.

<details><summary>Synchronous Usage Example</summary>

```python
import asyncio

from genesis_api_wrapper import AsyncGENESISWrapper

# Create a new wrapper with your credentials
_wrapper = AsyncGENESISWrapper(
    username="<<your-username-here>>",
    password="<<your-password-here>>"
)

# Get the current event loop
_loop = asyncio.get_event_loop()

# Execute a call in the loop which checks your credentials
call_result = _loop.run_until_complete(_wrapper.hello_world.login_check())
```
</details>

### Create a new wrapper
To be able to use the wrapper you first need to instantiate a new wrapper object.

```python
from genesis_api_wrapper import AsyncGENESISWrapper

# Create a new instance of the wrapper and its functions
_wrapper = AsyncGENESISWrapper(
    username="<<your-username-here>>",
    password="<<your-password-here>>"
)
```

After instantiating the new wrapper you are able to access all methods under their respective 
service. 

<details><summary>The following services are available:</summary>

| Service Name | Property of the wrapper | Description                                                                                                   |
|--------------|-------------------------|---------------------------------------------------------------------------------------------------------------|
| Hello World  | `hello_world`           | Methods for testing the access to the API (User Agent Check/Credential Validation)                            |
| Find         | `find`                  | Methods for finding objects stored in the database (Tables, Statistics, Variables, Data Cubes and Timeseries) |
| Catalogue    | `catalogue`             | Methods for listing objects                                                                                   |
| Data         | `data`                  | Methods for downloading data                                                                                  |
| ~~Metadata~~ | `metadata`              | Methods for downloading metadata about objects in the database                                                |
| ~~Profile~~  | `profile`               | Methods for maintaining the own user account                                                                  |
</details>
