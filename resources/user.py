from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_jwt_extended import create_access_token, jwt_required, get_jwt

from db import db
from blocklist import BLOCKLIST

from models import UserModel
from schemas import UserSchema

blp = Blueprint('Users', __name__, description="Operations on users")

@blp.route('/register')
class RegisterUser(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel(
            username=user_data['username'],
            password=pbkdf2_sha256.hash(user_data['password'])
        )

        try:
            db.session.add(user)
            db.session.commit()
        
        except IntegrityError:
            db.session.rollback()
            abort(400, message='A user with that name aready exists.')

        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message='An error occurred whilst inserting the user to the database.')    

        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

        return {"meesage": "User created successfully"}, 201
    
@blp.route('/login')
class UserLogin(MethodView):
    @blp.arguments(UserSchema)
    def post(self, user_data):
        user = UserModel.query.filter_by(username=user_data['username']).first()

        if user and pbkdf2_sha256.verify(user_data['password'], user.password):
            access_token = create_access_token(identity=user.id)
            #access_token = 'Token'
            return {"access_token": access_token}, 200

        abort(401, message="Invalid credentials")

@blp.route('/logout')
class UserLogout(MethodView):
    @jwt_required()
    def post(self):
        jti = get_jwt()['jti']
        BLOCKLIST.add(jti)
        return {"message": "Successfully logged out"}, 200
    
@blp.route('/user/<int:user_id>')
class User(MethodView):
    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted successfully"}, 200

