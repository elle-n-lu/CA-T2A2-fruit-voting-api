from flask_jwt_extended import  jwt_required
from flask import Blueprint, render_template, request
from pkg_init import db
from controllers.admin_ctl import admin_required
from controllers.user_ctl import owner_required
from models.orders import Order, OrderSchema
from models.cinema import Cinema
from flask_login import login_required,current_user



app_order = Blueprint("orders", __name__)

# create order
@app_order.route("/users/<int:user_id>/cinemas/<int:cinema_id>/orders", methods=['POST'])
@jwt_required()
def create_sorder(cinema_id, user_id):
    # check user login
    owner_required(user_id)
    cinema=Cinema.query.filter_by(id=cinema_id).first()
    if not cinema:
        return {"error":"cinema not exist"}
    # add order data in db
    order = OrderSchema().load(request.form)
    new_order = Order(
        movie_name=order["movie_name"],
        schedule = order['schedule'],
        session = order['session'],
        seat = order['seat'],
        user_id = user_id,
        cinema_id = cinema_id,
        admin_id= 1
    )
    db.session.add(new_order)
    db.session.commit()
    # return a value to show or use
    return OrderSchema().dump(new_order), 201

'''
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

# delete single order
@app_order.route("/orders/<int:order_id>",methods=['DELETE'])
@jwt_required()
def delete_order(order_id):
    # check user authorization
    owner_required()

    # check if order exist
    order_c=order_check(order_id)
    # delete order
    db.session.delete(order_c)
    db.session.commit()
    return "order deleted"
