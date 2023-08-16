from datetime import date
from flask_jwt_extended import  jwt_required
from controllers.seat_ctl import get_seats
from flask import Blueprint, flash, redirect, render_template, request, url_for
from controllers.movie_ctl import get_all_movies
from controllers.cinema_ctl import get_cinemas
from pkg_init import db
from controllers.admin_ctl import admin_required
from models.movies import Movie
from models.schedules import Schedule, ScheduleSchema
from flask_login import login_required,current_user


app_schedule = Blueprint("schedules", __name__)

# create a schedule, only admin allowed
@app_schedule.route("/cinema/<int:cinema_id>/movie/<int:movie_id>'/schedules", methods=['POST'])
@jwt_required()
def create_schedule(cinema_id, movie_id):
    # check admin login
    admin_required()
    movie=Movie.query.filter_by(id=movie_id).first()
    if not movie:
        return {"error":"movie not exist"}
    # add schedule data in db
    schedule = ScheduleSchema().load(request.form)
    new_schedule = Schedule(
        schedule_date=schedule["schedule_date"],
        movie_id = movie_id
    )
    db.session.add(new_schedule)
    db.session.commit()
    # return a value to show or use
    return ScheduleSchema().dump(new_schedule), 201


'''
in-use
'''
@app_schedule.route("/ajax_schedules/<int:a>/<int:b>/<int:c>", methods=['GET'])
def get_all_schedules(a,b,c):
    stmt=db.select(Schedule).filter_by(cinema_id=a, seat_id=b, movie_id=c)
    print('stm',stmt)
    schedule=db.session.scalars(stmt)
    posts =  ScheduleSchema(many=True).dump(schedule)
    return posts

# retrieve all orders
@app_schedule.route("/schedules",methods=('GET', 'POST'))
@login_required
def get_schedules():
    if request.method == 'POST':
        cinema_id = request.form['cinema_id']
        schedule_date = request.form['schedule_date']
        movie_id = request.form['movie_id']
        seat_id = request.form['seat_id']
        new_schedule= Schedule(
            schedule_date=schedule_date,
            cinema_id=cinema_id,
            movie_id=movie_id,
            seat_id = seat_id
        )
        # toast='schedule added !'    
        db.session.add(new_schedule)
        db.session.commit()
        return redirect(url_for('schedules.get_schedules'))
    today_date = date.today()
    cinemas=get_cinemas()
    seats=get_seats()
    if not cinemas or not seats:
        return render_template('cinema/all_schedules.html',)
    movies=get_all_movies(cinemas[0]['id'],seats[0]['id'])
    return render_template('cinema/all_schedules.html', today_date=today_date, cinemas=cinemas,movies=movies,user=current_user.username)

'''

'''

def schedule_check(schedule_id,cinema_id, movie_id,seat_id):
    schedule_check=Schedule.query.filter_by(seat_id=seat_id,id=schedule_id,cinema_id=cinema_id,movie_id=movie_id).first()
    if not schedule_check:
        return {"error":"schdule for this movie not exist"}
    return schedule_check
        
'''
# retrieve single schedule data
@app_schedule.route("/schedules/<int:schedule_id>", methods=['GET'])
def get_schedule(schedule_id,movie_id,cinema_id):
    # check if schedule exist, error if not
    schedule = schedule_check(schedule_id)
    return ScheduleSchema().dump(schedule)

# update single schedule
@app_schedule.route("/schedules/<int:schedule_id>",methods=['PUT'])
@jwt_required()
def update_schedule(schedule_id,movie_id,cinema_id):
    # check admin authorization
    admin_required()
     # check if schedule exist , error if not
    schedule_c = schedule_check(schedule_id)
    # get use input
    new_schedule= ScheduleSchema().load(request.form)
    # update schedule 
    schedule_c.schedule_date=new_schedule["schedule_date"]
    db.session.commit()
    return ScheduleSchema().dump(schedule_check), 201

'''

# delete single schedule
@app_schedule.route("/schedules/delete",methods=['POST'])
# @jwt_required()
def delete_schedule():
    # check admin authorization
    # admin_required()
    schedule_id = request.form['schedule_id']
    cinema_id = request.form['cinema_id']
    movie_id = request.form['movie_id']
    seat_id = request.form['seat_id']
    # check if schedule exist
    schedule_c = schedule_check(schedule_id,cinema_id, movie_id, seat_id)
    # delete movie
    db.session.delete(schedule_c)
    db.session.commit()
    return redirect(url_for('schedules.get_schedules'))
