from sqlalchemy import exc
from datetime import timedelta
from flask import Blueprint, abort, jsonify, request
from models.users import User, UserSchema
from pkg_init import db, bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity

app_auth=Blueprint("auth",__name__)

def admin_required():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user=db.session.scalar(stmt)
    if not (user and user.admin):
        abort(401)

def admin_or_owner_required(owner_id):
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user=db.session.scalar(stmt)
    if not (user and (user.admin or user_id==owner_id)):
        abort(401)

@app_auth.route("/users",methods=['GET'])
def get_users():
    stmt=db.select(User)
    users=db.session.scalars(stmt)
    return UserSchema(many=True, exclude=['password']).dump(users)
    # users = User.query.all()
    # res=UserSchema(many=True,exclude=['password']).dump(users)
    # return jsonify(res)

@app_auth.route("/registe",methods=['POST'])
def registe_users():
    try:
        user_info = UserSchema().load(request.form)
        user=User(
            username=user_info['username'],
            email=user_info['email'],
            password=bcrypt.generate_password_hash(user_info['password']).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        return UserSchema(exclude=['password']).dump(user), 201
    except exc.IntegrityError:
        return {'error':'email already exist'},409
    except KeyError:
        return {'error':'missing data required'}

@app_auth.route("/login/",methods=['POST'])
def login_users():   
    try:    
        user_info=UserSchema().load(request.form)
        user=User.query.filter_by(email=user_info['email']).first()
        # stmt=db.select(User).filter_by(email=request.json['email'])
        # user=db.session.scalar(stmt)
        if not user :
            return {"error":"user not exist"},404
        elif not bcrypt.check_password_hash(user.password,user_info['password']):
            return {"error":"Incorrect username and password"}, 402
        
        expire=timedelta(days=1)
        access_token=create_access_token(identity=user.id,expires_delta=expire)
        return {"user":user.username,"id":user.id, "token":access_token}
    except KeyError:
        return {"error":"email and password are required"}, 400
   



