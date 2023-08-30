from controllers.user_ctl import user_login_required
from flask_jwt_extended import  jwt_required
from flask import Blueprint, redirect, render_template, request, url_for
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
def fetch_sold_seats(sessionId):
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
        total_price=order['total_price'],
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
@app_order.route("/orders/alll",methods=['GET'])
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

@app_order.route("/orders/users/<int:user_id>",methods=['GET'])
def get_user_orders(user_id):
    order_c=Order.query.filter_by(user_id=user_id)
    orders= OrderSchema(many=True,exclude=("user",)).dump(order_c)
    return orders


@app_order.route("/orders/<int:id>/delete",methods=('GET','POST'))
@login_required
def delete_a_order(id):
    if request.method == 'POST':
        order_check=Order.query.filter_by(id=id).first()
        db.session.delete(order_check)
        db.session.commit()
        return redirect(url_for('orders.get_orders'))
    return render_template('cinema/delete_order.html', user=current_user.username)

