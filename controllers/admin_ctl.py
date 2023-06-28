from datetime import timedelta
from flask import Blueprint, abort, request, jsonify
from pkg_init import db, bcrypt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from models.admin import Admin, AdminSchema
from models.users import User, UserSchema

app_admin=Blueprint("admin",__name__)

# admin login function check
def admin_required():
    user_id = get_jwt_identity()
    stmt = db.select(Admin).filter_by(id=user_id)
    user=db.session.scalar(stmt)
    if not (user and user.admin):
        abort(401)
    else:
        return user
    
# admin login
@app_admin.route("/admin",methods=['POST'])
def admin_login():
    # retrieve input data
    user_info=AdminSchema().load(request.form)
    user=Admin.query.filter_by(email=user_info['email']).first()
    # error if admin not exist
    print(user.password,user_info['password'],'sad',bcrypt.check_password_hash(user.password,user_info['password']))
    if not user :
        return {"error":"user not exist"},404
    # error if password incorrect
    elif not bcrypt.check_password_hash(user.password,user_info['password']):
        return {"error":"Incorrect username and password"}, 402
    # generate token for further use
    expire=timedelta(days=1)
    access_token=create_access_token(identity=user.id,expires_delta=expire)
    # return data for further use
    return {"user":user.username,"id":user.id, "token":access_token}

# update user info
@app_admin.route("/admin",methods=['PUT'])
@jwt_required()
def update_user():
    # check admin login
    admin=admin_required()
    # get use input
    user_info= AdminSchema().load(request.form)
    # update user information
    admin.username= user_info.get("username", admin.username)
    if user_info.get("password", admin.password) != admin.password:
        admin.password=bcrypt.generate_password_hash(user_info.get("password", admin.password)).decode('utf-8')
    admin.email=user_info.get("email", admin.email)
    db.session.commit()
    return AdminSchema().dump(admin), 201

# retrieve all customers' data 
@app_admin.route("/admin/users",methods=['GET'])
@jwt_required()
def get_users():
    admin=admin_required()
    users = User.query.all()
    res=UserSchema(many=True,exclude=['password','comments','votes']).dump(users)
    return jsonify(res)


