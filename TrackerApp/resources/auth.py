import datetime 
from flask import request
from TrackerApp.models import User
from flask_restful import Resource
from TrackerApp import db
from flask_jwt_extended import create_access_token

class SignupApi(Resource):
    def post(self):
        body = request.get_json()
        user = User(**body)
        
        if User.query.filter_by(username=user.username).first():
            msg = "Username already exists, login or use a different Username to Register"
            return {'msg': msg}, 401

        db.session.add(user)
        db.session.commit()
        return {'msg': "User now Registered"}, 200

class LoginApi(Resource):

    def post(self):
        body = request.get_json()

        user = User.query.filter_by(username=body.get('Username')).first()
        authorized = user.check_password(body.get('Password'))
        
        if not authorized:
            return {'msg': 'Username or password invalid'}, 401

        expires = datetime.timedelta(days=365)
        access_token = create_access_token(identity=str(user.id), expires_delta=expires)
        
        return {'token': access_token}, 200