from flask_jwt_extended import  jwt_required
from flask import Blueprint, redirect, render_template, request, url_for
from controllers.cinema_ctl import get_cinemas

from flask_login import login_required
from pkg_init import db
from controllers.admin_ctl import admin_required
from models.sessions import Session
from models.seats import Seat, SeatSchema


app_seat = Blueprint("seats", __name__)
'''
views: in-use
'''
def get_seats():
    stmt=db.select(Seat)
    seats=db.session.scalars(stmt)
    totalseats = SeatSchema(many=True,).dump(seats)
    return totalseats

@app_seat.route("/seats",  methods=('GET', 'POST'))
@login_required
def create_total_seat():
    if request.method == 'POST':
        cinema_id = request.form['cinema_id']
        seat_number = request.form['seat_number']
        new_seat = Seat(
            seat_number=seat_number,
            cinema_id = cinema_id
        )
        db.session.add(new_seat)
        db.session.commit()
        return redirect(url_for('seats.create_total_seat',))
    cinemas = get_cinemas()
    totalseats = get_seats()
    return render_template('cinema/seats.html', seats=totalseats, cinemas=cinemas)

@app_seat.route("/ajax_seats/<int:a>", methods=['GET'])
def get_all_seats_by_cinema(a):
    stmt=db.select(Seat).filter_by(cinema_id=a)
    session=db.session.scalars(stmt)
    seats =  SeatSchema(many=True).dump(session)
    return seats

@app_seat.route("/cinemas/<int:cinema_id>/seats/<int:id>/delete",methods=('GET','POST'))
@login_required
def delete_a_seat(cinema_id,id):
    if request.method == 'POST':
        seat_check=Seat.query.filter_by(id=id,cinema_id=cinema_id).first()
        db.session.delete(seat_check)
        db.session.commit()
        return redirect(url_for('seats.create_total_seat'))
    return render_template('cinema/update_seat.html')

'''

'''
# create a seat, only admin allowed
@app_seat.route("/cinema/<int:cinema_id>/movie/<int:movie_id>/schedule/<int:schedule_id>/session/<int:session_id>/seats", methods=['POST'])
@jwt_required()
def create_seat(session_id,cinema_id, movie_id, schedule_id):
    # check admin login
    admin_required()
    session=Session.query.filter_by(id=session_id).first()
    if not session:
        return {"error":"session not exist"}
    # add seat data in db
    seat = SeatSchema().load(request.form)
    new_seat = Seat(
        seat_number=seat["seat_number"],
        session_id = session_id
    )
    db.session.add(new_seat)
    db.session.commit()
    # return a value to show or use
    return SeatSchema().dump(new_seat), 201

# retrieve all seat data
@app_seat.route("/cinema/<int:cinema_id>/movie/<int:movie_id>/schedule/<int:schedule_id>/session/<int:session_id>/seats",methods=['GET'])
def get_seat_s(session_id,cinema_id, movie_id, schedule_id):
    stmt=db.select(Seat)
    seats=db.session.scalars(stmt)
    return SeatSchema(many=True,).dump(seats)

# retrieve single seat data
# @app_seat.route("/seats/<int:seat_id>", methods=['GET'])
# def get_seat(seat_id):
#     # check if seat exist, error if not
#     seat_c=Session.query.filter_by(id=seat_id).first()
#     return SeatSchema().dump(seat_c)

'''
后面看情况删掉该update route
可能不需要这个route, 如果修改也就是反选，就直接删除在数据库中的数据
投票不一样的是有两个选项, 这里是选了就存, 不选就不存。 
不存数据在前端就没有信息
'''
# update single seat
# @app_seat.route("/seats/<int:seat_id>",methods=['PUT'])
# @jwt_required()
# def update_seat(seat_id):
#     # check admin authorization
#     admin_required()
#      # check if seat exist , error if not
#     seat_c=Session.query.filter_by(id=seat_id).first()
#     # get use input
#     new_seat= SeatSchema().load(request.form)
#     # update seat 
#     seat_c.seat_number=new_seat["seat_number"]
#     seat_c.seat_status=new_seat["seat_status"]
#     db.session.commit()
#     return SeatSchema().dump(seat_c), 201

'''
反选就删除数据库信息
'''
# delete single seat
@app_seat.route("/cinema/<int:cinema_id>/movie/<int:movie_id>/schedule/<int:schedule_id>/session/<int:session_id>/seats/<int:seat_id>",methods=['PUT'])
@jwt_required()
def delete_seat(seat_id,cinema_id, movie_id, schedule_id):
    # check admin authorization
    admin_required()

    # check if seat exist
    seat_c=Session.query.filter_by(id=seat_id).first()
    # delete seat
    if seat_c:
        db.session.delete(seat_c)
        db.session.commit()
        return "seat deleted"
    else:
        return
