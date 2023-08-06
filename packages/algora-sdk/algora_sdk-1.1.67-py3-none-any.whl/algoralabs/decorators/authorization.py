"""
Module containing algoralabs' authorization decorators
"""
import functools
import json
import logging
import requests
from typing import Tuple, Dict, Any, Callable, Optional
from cachetools import cached, TTLCache

from algoralabs.common.config import EnvironmentConfig
from algoralabs.common.errors import AuthenticationError

logger = logging.getLogger(__name__)


# TODO: Figure out max size
@cached(cache=TTLCache(maxsize=100, ttl=1740))
def authenticate(
        base_url: Optional[str],
        username: Optional[str],
        password: Optional[str],
        token: Optional[str]
) -> dict:
    """
    Authenticates a user and creates a users auth headers

    Args:
        base_url: URL for signing a user in
        username:
        password:
        token:

    Returns:
        Auth headers for a request
    """
    auth_headers = {}
    if token:
        auth_headers = _auth_token(token)
    elif username and password:
        auth_headers = _sign_in(
            base_url=base_url,
            username=username,
            password=password
        )
    return auth_headers


def _sign_in(base_url: str, username: str, password: str) -> dict:
    auth_response = requests.post(
        url=f"{base_url}/login",
        data=json.dumps({"username": username, "password": password}),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
    )

    if auth_response.status_code == 200:
        bearer_token = auth_response.json()['access_token']
        return {'Authorization': f'Bearer {bearer_token}'}
    else:
        error = AuthenticationError("Failed to authenticate the user")
        logger.error(error)
        raise error


def _auth_token(token: str) -> dict:
    return json.loads(token)


def authenticated_request(
        request: Callable = None,
        *,
        env_config: Optional[EnvironmentConfig] = None
) -> Callable:
    """
    Decorator for requests that need to be authenticated

    Args:
          request: Method that need auth headers injected into it
          env_config: Optional environment config
    """
    @functools.wraps(request)
    def decorator(f):
        @functools.wraps(f)
        def wrap(*args: Tuple, **kwargs: Dict[str, Any]) -> Any:
            """
            Wrapper for the decorated function

            Args:
                *args: args for the function
                **kwargs: keyword args for the function

            Returns:
                The output of the wrapped function
            """
            config = env_config if env_config is not None else EnvironmentConfig()
            headers = kwargs.get("headers", {})

            if config.auth_config.can_authenticate():
                auth_headers = authenticate(
                    base_url=config.get_url(),
                    username=config.auth_config.username,
                    password=config.auth_config.password,
                    token=config.auth_config.token
                )
                auth_headers.update(headers)  # override authentication header if already provided
                kwargs["headers"] = auth_headers
            elif headers.get("Authorization") is None:
                error = AuthenticationError("Authentication for the package was configured incorrectly and is either "
                                            "missing a AUTH_TOKEN or ALGORA_USER and ALGORA_PWD environment variable(s)")
                logger.error(error)

            return f(*args, **kwargs)

        return wrap

    if request is None:
        return decorator
    return decorator(request)
