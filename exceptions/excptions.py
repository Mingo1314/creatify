class CreatifyException(Exception):
    def __init__(self, code='10500', message='服务器开小差了~', data=""):
        self.error_code = code
        self.error_message = message
        self.data = data


class EmailFormatException(CreatifyException):
    def __init__(self, data=""):
        self.error_message = '邮箱格式错误'
        self.error_code = '10501'
        self.data = data


class PasswordFormatException(CreatifyException):
    def __init__(self, data=""):
        self.error_message = '密码格式错误, 请输入8-20位字符，必须包含字母及数字'
        self.error_code = '10502'
        self.data = data


class EmailExistException(CreatifyException):
    def __init__(self, data=""):
        self.error_message = '该Email已存在'
        self.error_code = '10503'
        self.data = data


class AuthenticationException(CreatifyException):
    def __init__(self, data=""):
        self.error_message = '用户名或密码错误'
        self.error_code = '10504'
        self.data = data


class NotLoginException(CreatifyException):
    def __init__(self, data=""):
        self.error_message = '用户未登录'
        self.error_code = '10505'
        self.data = data


