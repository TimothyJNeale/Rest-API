from flask.views import MethodView
from flask_smorest import Blueprint, abort
from passlib.hash import pbkdf2_sha256
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from db import db
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
            abort(400, message='A store with that name aready exists.')

        except SQLAlchemyError:
            db.session.rollback()
            abort(500, message='An error occurred whilst inserting the store to the database.')    

        except Exception as e:
            db.session.rollback()
            abort(500, message=str(e))

        return {"meesage": "User created successfully"}, 201
    
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
