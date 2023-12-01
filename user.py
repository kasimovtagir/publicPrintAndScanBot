import requests
from logging import Logger, getLogger


class ServerError(Exception):
    def __str__(self):
        return "Server error (response.status_code not in (200, 201, 204))"


class NoTidError(Exception):
    def __init__(self, tid):
        self.tid = tid

    def __str__(self):
        return f"User tid={self.tid} has no access"


class User:
    def __init__(self, telegram_id: str="",
                 uid: str="",
                 roles_target_id: str="",
                 name: str = None,
                 second_name: str = None,
                 **kwargs):
        self.user_id = str(telegram_id)
        self.uid = str(uid)
        self.roles = [r for r in roles_target_id.split(',')]
        self.name = name
        self.second_name = second_name
        self.__dict__.update(kwargs)

    def __repr__(self):
        return str(self.__dict__)


class BadRoleError(Exception):
    def __init__(self, user: User):
        self.tid = user.user_id
        self.roles = user.roles
        self.uid = user.uid

    def __str__(self):
        return f"User tid={self.tid}, uid={self.uid}, roles=[{', '.join(self.roles)}] has no access due to role"


class UserAPI:
    def __init__(self, token: str, logger: Logger = None, timeout=10):
        self.token = token
        self.timeout = timeout
        self.session = requests.Session()
        self.logger = getLogger() if logger is None else logger
        self.test = False

    def request(self, url: str, params: list) -> dict or None or list:
        headers = {
            "Authorization": f"Bearer {self.token}"
        }

        response = self.session.request('GET', url,
                                        params=params,
                                        headers=headers,
                                        timeout=self.timeout)
        if response.status_code not in (200, 201, 204):
            
            self.logger.error(response.text)
            raise ServerError
        return response.json()

    def get_user_by_tid(self, user_tid: int) -> User:
        url = "https://physics.itmo.ru/ru/rest/export/json/users-telegram-id-roles"
        params = [
            ("_format", "json"),
            ("telegram_id_value", user_tid)
        ]
        u = self.request(url=url, params=params)  # type: list
        if len(u) == 0:
            raise NoTidError(user_tid)
        
        user = User(**u[0])
        
        if 'member' not in user.roles:
            raise BadRoleError(user)
        return user