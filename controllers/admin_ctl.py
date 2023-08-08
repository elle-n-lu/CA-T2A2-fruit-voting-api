from datetime import timedelta
import os
from flask import Blueprint, abort, flash, make_response, redirect, render_template, request, jsonify,session, url_for
from pkg_init import db, bcrypt
import jwt
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required,create_refresh_token , set_access_cookies, set_refresh_cookies
from models.admin import Admin, AdminSchema
from models.users import User, UserSchema
from models.orders import Order, OrderSchema
from flask_login import login_user,login_required,current_user, logout_user

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
@app_admin.route("/admin",methods=('GET', 'POST'))
def admin_login():
    # user_token = session.get('user_token')
    
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user =Admin.query.filter_by(email=username).first()
        # print('user', user, user.email)
        if user is None:
            error = 'Incorrect username.'
        elif not bcrypt.check_password_hash(user.password, password):
            error = 'Incorrect password.'

        if error is None:
            # session.clear()
            expire=timedelta(days=1)
            access_token=create_access_token(identity=user.id,expires_delta=expire)
            refresh_token = create_refresh_token(identity=user.id,expires_delta=expire)
            # session['user_token'] = access_token
            login_user(user, remember=True)
            return redirect(url_for('cinema.get_cinema'))
            # resp = make_response(redirect(url_for('cinema.get_cinema')))
            # resp.set_cookie('resp', access_token)
            # # set_refresh_cookies(resp, refresh_token)
            # return resp

        flash(error)
    return render_template('auth/login.html')
    
    '''
    # retrieve input data
    user_info=AdminSchema().load(request.form)
    user=Admin.query.filter_by(email=user_info['email']).first()
    # error if admin not exist
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
    
    '''


@app_admin.route('/logout')
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for('admin.admin_login'))        





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
@login_required
def get_users():
    # admin=admin_required()
    users = User.query.all()
    res=UserSchema(many=True,exclude=['password','comments','votes']).dump(users)
    # return jsonify(res)
    return render_template('cinema/all_users.html', users=res,user=current_user.username)



