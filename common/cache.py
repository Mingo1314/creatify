"""
暂时使用程序内存 存储用户的token， 后续改成redis
"""
import jwt
import time
from typing import Dict,  Union, Any

from django.conf import settings


ALGORITHM = "HS512"
ACCESS_TOKEN_EXPIRE = 86400 * 1  # one day
REFRESH_TOKEN_EXPIRE = 86400 * 7  # one day
ALL_TOKENS = {}


def set_jwt_token(user_id: int, email: str):
    global ALL_TOKENS
    access_token = create_access_token_for_user(email, settings.SECRET_KEY, ACCESS_TOKEN_EXPIRE)
    refresh_token = create_access_token_for_user(email, settings.SECRET_KEY, REFRESH_TOKEN_EXPIRE)
    ALL_TOKENS[access_token[0]] = user_id
    ALL_TOKENS[refresh_token[0]] = user_id
    return {"access_token": access_token, "refresh_token": access_token}


def check_login(access_token: str) -> Union[int, None]:
    print(access_token, ALL_TOKENS)
    if access_token in ALL_TOKENS:
        # TODO 过期确认
        return ALL_TOKENS[access_token]
    return None


def create_jwt_token(
        *,
        jwt_content: Dict[str, Any],
        secret_key: str,
        expires: int,
) -> str:
    iat = int(time.time())
    expire = iat + expires
    jwt_content.update({"exp": expire, "iat": iat})
    return jwt.encode(jwt_content, secret_key, algorithm=ALGORITHM), expire


def create_access_token_for_user(email: str, secret_key: str, expires: int) -> str:
    return create_jwt_token(
        jwt_content={"sub": email},
        secret_key=secret_key,
        expires=expires
    )




