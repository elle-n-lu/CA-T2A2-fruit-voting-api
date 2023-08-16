from controllers.user_ctl import user_login_required
from flask_jwt_extended import  jwt_required
from flask import Blueprint, render_template, request
from pkg_init import db
from controllers.admin_ctl import admin_required
from controllers.user_ctl import owner_required
from models.orders import Order, OrderSchema
from models.sessions import Session
from models.cinema import Cinema
from flask_login import login_required,current_user
from sqlalchemy import exc, select
from sqlalchemy import func


app_order = Blueprint("orders", __name__)

@app_order.route('/orders/<int:sessionId>', methods=['GET'])
def fetch_seats(sessionId):
    # orders=Order.query.filter_by(session_id=sessionId).first()
    # seats= OrderSchema(many=True,).dump(orders)
    stmt = (
            select( Order.seat, func.count(Order.seat))
            .join_from(Order, Session)
            .group_by(Order.seat,Order.id,Session.id)
            .having(Order.session_id==sessionId)
            )
    orders=db.session.scalars(stmt).all()
    s=''
    for i in orders:
        s += i+','
        
    return s.split(',')[:-1]
    # return orders


# create order
@app_order.route("/orders/create_new/<int:cinema_id>/<int:session_id>", methods=['POST'])
@jwt_required()
def create_order(cinema_id, session_id):
    # check user login
    user_id = user_login_required()
    # add order data in db
    order = OrderSchema().load(request.form)
    new_order = Order(
        seat = order['seat'],
        user_id = user_id,
        cinema_id = cinema_id,
        admin_id= 1,
        session_id = session_id
    )
    db.session.add(new_order)
    db.session.commit()
    # return a value to show or use
    return OrderSchema().dump(new_order), 201

'''
views
admin get all orders of all users
'''
def get_order_ss():
    stmt=db.select(Order)
    orders=db.session.scalars(stmt)
    orderss= OrderSchema(many=True,).dump(orders)
    return orderss

# retrieve all orders
@app_order.route("/orders",methods=['GET'])
@login_required
def get_orders():
    orderss = get_order_ss()
    return render_template('cinema/all_orders.html',orders=orderss,user=current_user.username)


def order_check(order_id):
    order_check=Order.query.filter_by(id=order_id).first()
    if not order_check:
        return {"error":"order not exist"}
    return order_check


'''
# retrieve single order data
@app_order.route("/orders/<int:order_id>", methods=['GET'])
def get_order(order_id):
    # check if order exist, error if not
    order_c = order_check(order_id)
    return OrderSchema().dump(order_c)

# update single order
@app_order.route("/orders/<int:order_id>",methods=['PUT'])
@jwt_required()
def update_order(order_id):
    # check user authorization
    owner_required()
     # check if order exist , error if not
    order_c=order_check(order_id)
    # get use input
    new_order= OrderSchema().load(request.form)
    # update order 
    order_c.movie_name=new_order["movie_name"]
    order_c.schedule=new_order["schedule"]
    order_c.session=new_order["session"]
    order_c.seat=new_order["seat"]
    db.session.commit()
    return OrderSchema().dump(order_c), 201
'''
@app_order.route("/orders/<int:order_id>",methods=['PUT'])
# @login_required
def update_order(order_id):
    # check if order exist , error if not
    # user=current_user.username
    order_c=order_check(order_id)
    # get use input
    new_order= OrderSchema().load(request.form)
    # update order 
    order_c.seat=new_order["seat"]
    db.session.commit()
    return OrderSchema().dump(order_c), 201

# delete single order
@app_order.route("/orders/<int:order_id>",methods=['DELETE'])
# @jwt_required()
def delete_order(order_id):
    # check user authorization
    # owner_required()

    # check if order exist
    order_c=order_check(order_id)
    # delete order
    db.session.delete(order_c)
    db.session.commit()
    return "order deleted"
