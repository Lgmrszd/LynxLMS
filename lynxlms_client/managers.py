import requests
import json
from lynxlms_client import config

_headers = {'Content-type': 'application/json'}
_url = config.get_url()


class User:
    user_id = 0
    name = ""
    surname = ""
    address = ""
    phone = 0
    fine = 0
    group = 0
    active = False

    _create_values = ["name", "surname", "address", "phone", "group"]
    _class_url = "lynx_lms/api/users"

    def __init__(self, **kwargs):
        for k in self._create_values:
            if k not in kwargs.keys():
                raise TypeError
        args = self._post_user(kwargs)
        print(args)
        for k, v in args.items():
            setattr(self, k, v)

    @classmethod
    def get_user_by_id(cls, user_id):
        response = requests.get("%s/%s/%s" % (_url, cls._class_url, str(user_id)), headers=_headers)
        result = response.json()
        if response.status_code != 200:
            raise IndexError
        user = User.__new__(User)
        for k, v in result["user"].items():
            setattr(user, k, v)
        return user


    @classmethod
    def _post_user(cls, args):
        response = requests.post("%s/lynx_lms/api/users" % _url, headers=_headers, json=args)
        result = response.json()
        if response.status_code != 201:
            raise TypeError
        return result["user"]


if __name__ == '__main__':
    # u = User.get_user_by_id(2)
    u = User(
        name="Client Name",
        surname="Surname",
        address="Address",
        phone=1234,
        group=1
    )
    print(u.name, u.user_id)
    u1 = User.get_user_by_id(30)
    print(u1.name, u1.user_id)
