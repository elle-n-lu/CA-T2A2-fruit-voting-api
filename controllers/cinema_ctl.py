
import os
from flask_jwt_extended import  jwt_required
import jwt
from controllers.order_ctl import get_order_ss
from models.admin import Admin
from sqlalchemy import exc
from flask import Blueprint, redirect, render_template, request, session, url_for
from pkg_init import db
from controllers.admin_ctl import admin_required
from models.cinema import CinemaSchema, Cinema
from flask_login import login_required,current_user

app_cinema=Blueprint("cinema",__name__)

# retrieve all cinema data

@app_cinema.route("/cinemas",methods=('GET',))
def get_cinemas():
    stmt=db.select(Cinema)
    cinema=db.session.scalars(stmt)
    posts =  CinemaSchema(many=True,exclude=['admin_id',]).dump(cinema)
    return posts
'''
in-use
views
'''
@app_cinema.route("/all_cinemas",methods=('GET', 'POST'))
@login_required
def get_cinema():
    if request.method == 'POST':
        cinema_name = request.form['cinema_name']
        
        new_cinema= Cinema(
            cinema_name=cinema_name,
            admin_id=1
        )
        db.session.add(new_cinema)
        db.session.commit()
        return redirect(url_for('cinema.get_cinema'))
        
    posts = get_cinemas()
    return render_template('cinema/all_cinames.html', posts=posts,user=current_user.username)


'''
waiting for adding ????????-------???????
'''
# update single specie
@app_cinema.route("/cinema/<int:cinema_id>",methods=['PUT'])
@jwt_required()
def update_cinema(cinema_id):
    # check admin authentication
    admin_required()
    # check if cinema exist
    cinema_check=Cinema.query.filter_by(id=cinema_id).first()
    # get use input
    specie= CinemaSchema().load(request.form)
    if not cinema_check:
        return {"error":"cinema not found"}
    # update cinema name
    cinema_check.cinema_name=specie.get("cinema_name", cinema_check.cinema_name)
    db.session.commit()
    return CinemaSchema().dump(cinema_check), 201

# delete single cinema
@app_cinema.route("/cinema/<int:cinema_id>",methods=['DELETE'])
@jwt_required()
def delete_cinema(cinema_id):
    # check admin authentication
    admin_required()
    # check if cinema exist
    cinema_check=Cinema.query.filter_by(id=cinema_id).first()
    if not cinema_check:
        return {"error":"cinema not found"}
    # delete cinema
    db.session.delete(cinema_check)
    db.session.commit()
    return "cinema deleted"