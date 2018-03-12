from lynxlms_server import *
from flask import Flask
from flask_restful import Api


def tests():
    Librarian.create(
        name="LibrName",
        surname="LibrSurname",
        password="Password"
    )
    for i in range(60):
        j = str(i)+" "
        User.create(
            name=j+"Name",
            surname=j+"Surname",
            address=j+"Address",
            phone=14241,
            group=Group.get(Group.name == "Students")
        )
    # Session.create(
    #     librarian=l
    # )


def main():
    config.init_main()
    tests()
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(UserAPI, '/lynx_lms/api/users/<int:user_id>', endpoint='user')
    api.add_resource(UsersListAPI, '/lynx_lms/api/users', endpoint='users')
    app.run(debug=True)


if __name__ == '__main__':
    main()
