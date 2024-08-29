from typing import Union
import re


def check_email(value: str) -> Union[None, str]:
    """特定参数检测
    """
    if not value:
        return None
    if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', str(value)):
        return value
    return None


def check_password(value):
    """ 检测登录密码格式，8-20位字母数字组合，允许输入个别特殊字符
    old: "^(?![0-9]+$)(?![a-zA-Z]+$)[0-9A-Za-z]{8,20}$"
    """
    if not value:
        return None
    if re.match("^(?=.*[a-zA-Z])(?=.*\d)[A-Za-z\d_\-.,~+=@$!#%*?&()]{8,20}$", str(value)):
        return value
    return None