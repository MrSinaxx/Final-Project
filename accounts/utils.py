import jwt
from datetime import datetime, timedelta
from uuid import uuid4
from django.conf import settings
from django.core.cache import cache
from typing import Any
from rest_framework.exceptions import APIException


class WrongToken(APIException):
    status_code = 401
    default_detail = "Not Acceptable"
    default_code = "403"


class TokenNotFound(APIException):
    status_code = 404
    default_detail = "Not Found"
    default_code = "403"


def access_token_gen(user_id: int):
    """Generate access token based on usser id."""

    access_token = token_encode(
        {
            "token_type": "access",
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(minutes=1),
            "iat": datetime.utcnow(),
            "jti": gen_jti(),
        }
    )

    return access_token


def refresh_token_gen(user_id: int):
    """Generate refresh token based on usser id."""

    refresh_token = token_encode(
        {
            "token_type": "refresh",
            "user_id": user_id,
            "exp": datetime.utcnow() + timedelta(days=1),
            "iat": datetime.utcnow(),
            "jti": gen_jti(),
        }
    )

    return refresh_token


def gen_jti():
    """Generate hexed unique id for user"""
    return str(uuid4().hex)


def token_encode(payload):
    """Encode tokens based on HS256 algorithm"""

    token = jwt.encode(
        payload=payload, key=settings.SECRET_KEY, algorithm="HS256"
    ).decode("utf-8")
    return token


def token_decode(token):
    """Dencode tokens based on HS256 algorithm"""

    payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
    return payload


def check_token_type(token):
    """Returns the type of the token(access/refresh)"""
    try:
        payload = jwt.decode(jwt=token, key=settings.SECRET_KEY, algorithms=["HS256"])
        token_type = payload["token_type"]
    except:
        return None

    return token_type


def token_deleter(user_id: int):
    """Checkes if a user has refresh token and then deletes it."""
    uid = f"user_{user_id}"
    all_keys = cache.keys("*")
    for i in all_keys:
        x = i.split(" ")
        if uid == x[0]:
            cache.delete(i)


def cache_setter(refresh_token: str) -> None:
    """Set a value in the cache with an optional expiration time."""

    token = token_decode(refresh_token)
    if token["token_type"] == "refresh":
        jti = token["jti"]
        id = token["user_id"]
        key = f"user_{id} {jti}"

        key_deleter(key=key)

        exp = token["exp"]
        iat = token["iat"]
        timeout = exp - iat

        cache.set(key=key, value=exp, timeout=timeout)
    else:
        raise WrongToken("Wrong token type")


def key_deleter(key: str):
    """Check for duplicate keys and delete them from redis when found."""

    uid = key.split(" ")
    all_keys = cache.keys("*")

    for i in all_keys:
        x = i.split(" ")
        if uid[0] == x[0]:
            cache.delete(i)


def check_cache(user_id: int):
    """Checks to see whether or not there is any cached data for this user ID."""
    uid = f"user_{user_id}"
    all_keys = cache.keys("*")
    for i in all_keys:
        x = i.split(" ")
        if uid == x[0]:
            return True
        else:
            return False


def cache_getter(user_id: int):
    """
    Takes in the user_id and returns the refresh_token if the cached key is not timed out.
    If it's timedout then the user needs to login again
    """
    try:
        uid = f"user_{user_id}"
        all_keys = cache.keys("*")
        for i in all_keys:
            x = i.split(" ")
            if uid == x[0]:
                exp = cache.get(i)
                u_uid = x[1]

        return recreate_refresh_token(user_id, exp, u_uid)
    except:
        raise TokenNotFound("User is not logged in.")


def recreate_refresh_token(user_id, exp, u_uid):
    """Recreate the cached refresh token."""

    refresh_token = token_encode(
        {
            "token_type": "refresh",
            "user_id": user_id,
            "exp": exp,
            "iat": datetime.utcnow(),
            "jti": u_uid,
        }
    )

    return refresh_token
