from datetime import timedelta
import os
from flask import Blueprint, request, abort, jsonify
from sqlalchemy import exc
from flask_mail import Message
from itsdangerous import URLSafeTimedSerializer
from pkg_init import db, bcrypt, mail
from models.users import User, UserSchema
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required

app_user=Blueprint("user",__name__)

serializer = URLSafeTimedSerializer(os.environ.get("SECRET_KEY"))

def generate_token(email):
    token = serializer.dumps(email, salt='reset-password')
    return token

def verify_reset_token(token):
    try:
        email = serializer.loads(token, salt='reset-password', max_age=3600)  # Token expiration set to 1 hour
    except:
        return None
    user=User.query.filter_by(email=email).first()
    return user

def send_reset_email(email):
    token= generate_token(email)
    msg = Message("reset password",
                  sender="from@example.com",
                  recipients=[email])
    msg.body= f'''http://127.0.0.1:5000/reset_password/{token}'''
    mail.send(msg)


# login check funtion
def login_required():
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user=db.session.scalar(stmt)
    if not (user):
        abort(401)
    return user_id

# owner check funtion when users delete or update 
def owner_required(owner):
    user_id = get_jwt_identity()
    stmt = db.select(User).filter_by(id=user_id)
    user=db.session.scalar(stmt)
    if not (user and user_id == owner):
        abort(401)
    return user_id

# retrieve all user's own data, comments, votes...
@app_user.route("/my",methods=['GET'])
@jwt_required()
def get_user_details():
    user_id = get_jwt_identity()
    user=User.query.filter_by(id=user_id).first()
    res=UserSchema(exclude=['password',]).dump(user)
    return jsonify(res)

# '--------------------------'

@app_user.route("/reset_password", methods=['GET','POST'])
def send_email():
    email=request.form['email']
    user_check=User.query.filter_by(email=email).first()
    if not user_check:
        return 'invalid email'
    # send reset email if user email exists in db
    send_reset_email(email)
    return 'please check your email inbox'

# '--------------------------'
@app_user.route("/reset_password/<token>", methods=['GET','POST'])
def reset_password(token):
    user= verify_reset_token(token)
    if not user:
        return {"error":"toekn expired"}
    reset_data=request.form['password']
    user.password=bcrypt.generate_password_hash(reset_data).decode('utf-8')
    db.session.commit()
    return {'msg':'password changed, login again !'}

# '--------------------------'

# update user info
@app_user.route("/my/<int:user_id>",methods=['PUT'])
@jwt_required()
def update_user(user_id):
    owner_required(user_id)
    # check if user already exist, error if not
    user_check=User.query.filter_by(id=user_id).first()
    # get use input
    user_info= UserSchema().load(request.form)
    if not user_check:
        return {"error":"user not found"}
    # update user information
    user_check.username=user_info.get("username", user_check.username)
    if user_info.get("password", user_check.password) != user_check.password:
        user_check.password=bcrypt.generate_password_hash(user_info.get("password", user_check.password)).decode('utf-8')
    user_check.email=user_info.get("email", user_check.email)
    db.session.commit()
    return UserSchema().dump(user_check), 201

# registe a new account
@app_user.route("/registe",methods=['POST'])
def registe_users():
    try:
        # retrieve requested data
        user_info = UserSchema().load(request.form)
        # add new user in db
        user=User(
            username=user_info['username'],
            email=user_info['email'],
            password=bcrypt.generate_password_hash(user_info['password']).decode('utf-8')
        )
        db.session.add(user)
        db.session.commit()
        # return value for using and checking
        return UserSchema(exclude=['password']).dump(user), 201
    # error if email already exists
    except exc.IntegrityError:
        return {'error':'email already exist'},409

# login
@app_user.route("/login",methods=['POST'])
def login_users():   
    # retrive user input
    user_info=UserSchema().load(request.form)
    # check if user exist filter by email
    user=User.query.filter_by(email=user_info['email']).first()
    # error if not exist
    if not user :
        return {"error":"user not exist"},404
    # error if password incorrect
    elif not bcrypt.check_password_hash(user.password,user_info['password']):
        return {"error":"Incorrect username and password"}, 402
    # generate token
    expire=timedelta(days=1)
    access_token=create_access_token(identity=user.id,expires_delta=expire)
    # session['user_token'] = access_token
    # resp = make_response(redirect(url_for('cinema.get_cinema')))
    # resp.set_cookie('resp', access_token)
    return {"user":user.username,"id":user.id, "token":access_token}
    
# delete user account
@app_user.route("/userdelete/<int:user_id>",methods=['DELETE'])
@jwt_required()
def delete_userself(user_id): 
    # owner_required(user_id) 
    # check if user exist
    user=User.query.filter_by(id=user_id).first()
    if not user:
        return {"error":"user not exist"}
    # delete user from db
    db.session.delete(user)
    db.session.commit()
    # return a success message
    return {"msg":"user deleted"}, 200


       