from controllers.seat_ctl import get_seats
from flask_jwt_extended import  jwt_required
from flask import Blueprint, redirect, render_template, request, url_for
from controllers.movie_ctl import get_all_movies
from controllers.schedule_ctl import get_all_schedules
from controllers.cinema_ctl import get_cinemas
from pkg_init import db
from controllers.admin_ctl import admin_required
from models.schedules import Schedule
from models.sessions import Session, SessionSchema
from flask_login import login_required,current_user


app_session = Blueprint("sessions", __name__)

def session_check(schedule_id,cinema_id, movie_id,session_id,seat_id):
    session_check=Session.query.filter_by(seat_id=seat_id,schedule_id=schedule_id,cinema_id=cinema_id,movie_id= movie_id,id=session_id).first()
    if not session_check:
        return {"error":"session for this schedule not exist"}
    return session_check
        
'''
in-use
'''
@app_session.route("/ajax_sessions/<int:a>/<int:b>/<int:c>/<int:d>", methods=['GET'])
def get_all_sessions(a,b,c,d):
    stmt=db.select(Session).filter_by(cinema_id=a,seat_id=b,movie_id=c,schedule_id=d)
    session=db.session.scalars(stmt)
    posts =  SessionSchema(many=True).dump(session)
    return posts

# retrieve single session data
@app_session.route("/sessions", methods=('GET', 'POST'))
@login_required
def get_sessions():
    all_sessions=[]
    for time in range(1,13):
        all_sessions.append(str(time)+':00 PM')
    if request.method == 'POST':
        price=request.form['price']
        cinema_id = request.form['cinema_id']
        schedule_id = request.form['schedule_id']
        movie_id = request.form['movie_id']
        session_time=request.form['session_time']
        seat_id=request.form['seat_id']
        new_session= Session(
            price=price,
            schedule_id=schedule_id,
            cinema_id=cinema_id,
            movie_id=movie_id,
            session_time=session_time,
            seat_id=seat_id
        )
        db.session.add(new_session)
        db.session.commit()
        return redirect(url_for('sessions.get_sessions'))
    cinemas=get_cinemas()
    seats = get_seats()
    if not seats or not cinemas:
        return render_template('cinema/all_sessions.html',)
    movies=get_all_movies(cinemas[0]['id'],seats[0]['id'])
    return render_template('cinema/all_sessions.html',seats=seats,all_sessions=all_sessions,cinemas=cinemas,movies=movies,user=current_user.username)



# delete single schedule
@app_session.route("/sessions/delete",methods=['POST'])
# @jwt_required()
def delete_session():
    # check admin authorization
    # admin_required()

    schedule_id = request.form['schedule_id']
    cinema_id = request.form['cinema_id']
    movie_id = request.form['movie_id']
    session_id = request.form['session_id']
    seat_id = request.form['seat_id']
    # check if schedule exist
    schedule_c = session_check(schedule_id,cinema_id, movie_id,session_id, seat_id)
    # delete movie
    db.session.delete(schedule_c)
    db.session.commit()
    return redirect(url_for('sessions.get_sessions'))
