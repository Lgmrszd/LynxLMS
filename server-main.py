from lynxlms_server import *
from flask import Flask, jsonify, abort, make_response
from flask_restful import Api, Resource, reqparse, fields, marshal
import peewee as pw


class UsersListAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('surname', type=str, location='json')
        self.reqparse.add_argument('address', type=str, location='json')
        self.reqparse.add_argument('phone', type=int, location='json')
        self.reqparse.add_argument('fine', type=int, location='json')
        self.reqparse.add_argument('group', type=int, location='json')
        self.reqparse.add_argument('page_size', type=int, location='json')
        self.reqparse.add_argument('page', type=int, location='json')
        super(UsersListAPI, self).__init__()

    def get(self):
        print("A")
        args = self.reqparse.parse_args()
        search_args = {k: v for k, v in args.items() if (v is not None) and (k not in ["page", "page_size"])}
        if args["page"]:
            page = args["page"]
        else:
            page = 1
        if args["page_size"]:
            page_size = args["page_size"]
        else:
            page_size = 15
        print(page, page_size, search_args)

    def post(self):
        args = self.reqparse.parse_args()
        create_args = {k: v for k, v in args.items() if (k not in ["page", "page_size", "fine"])}
        for k, v in create_args.items():
            if v == None:
                abort(400)
        print(create_args)
        user = User.create(**create_args)
        user_fields = user.get_fields()
        return {"user": user_fields}, 201


class UserAPI(Resource):
    def __init__(self):
        self.reqparse = reqparse.RequestParser()
        self.reqparse.add_argument('name', type=str, location='json')
        self.reqparse.add_argument('surname', type=str, location='json')
        self.reqparse.add_argument('address', type=str, location='json')
        self.reqparse.add_argument('phone', type=int, location='json')
        self.reqparse.add_argument('fine', type=int, location='json')
        self.reqparse.add_argument('group', type=int, location='json')
        super(UserAPI, self).__init__()

    def get(self, user_id):
        try:
            User.get(User.user_id == user_id)
        except:   # TODO: specify error
            abort(404)
        user = User.get(User.user_id == user_id)
        user_fields = user.get_fields()
        return {"user": user_fields}

    def put(self, user_id):
        try:
            User.get(User.user_id == user_id)
        except:   # TODO: specify error
            abort(404)
        args = self.reqparse.parse_args()
        update_args = {k: v for k, v in args.items() if v is not None}
        print(update_args)
        User.update(**update_args).where(User.user_id == user_id).execute()

    def delete(self, user_id):
        try:
            User.get(User.user_id == user_id)
        except:   # TODO: specify error
            abort(404)
        user = User.get(User.user_id == user_id)
        if not user.active:
            abort(404)
        user.active = False
        user.save()
        return {'result': True}


def main():
    config.init_main()
    l = Librarian.create(
        name="LibrName",
        surname="LibrSurname",
        password="Password"
    )
    l.save()
    u = User.create(
        name="Name",
        surname="Surname",
        address="Address",
        phone=14241,
        group=Group.get(Group.name == "Students")
    )
    u.save()
    # s = Session.create(
    #     librarian=l
    # )
    # s.save()
    app = Flask(__name__)
    api = Api(app)
    api.add_resource(UserAPI, '/lynx_lms/api/users/<int:user_id>', endpoint='user')
    api.add_resource(UsersListAPI, '/lynx_lms/api/users', endpoint='users')
    app.run(debug=True)


if __name__ == '__main__':
    main()
