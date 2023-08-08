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
'''
# create a schedule, only admin allowed
@app_session.route("/sessions", methods=['POST'])
@jwt_required()
def create_session(cinema_id, movie_id,schedule_id):
    # check admin login
    admin_required()
    schedule=Schedule.query.filter_by(id=schedule_id).first()
    if not schedule:
        return {"error":"schedule not exist"}
    # add schedule data in db
    session = SessionSchema().load(request.form)
    new_session = Session(
        session_time=session["session_time"],
        schedule_id = schedule_id
    )
    db.session.add(new_session)
    db.session.commit()
    # return a value to show or use
    return SessionSchema().dump(new_session), 201
'''

def session_check(schedule_id,cinema_id, movie_id,session_id):
    session_check=Session.query.filter_by(schedule_id=schedule_id,cinema_id=cinema_id,movie_id= movie_id,id=session_id).first()
    if not session_check:
        return {"error":"session for this schedule not exist"}
    return session_check
        
'''
in-use
'''
@app_session.route("/ajax_sessions/<int:a>/<int:b>/<int:c>", methods=['GET'])
def get_all_sessions(a,b,c):
    stmt=db.select(Session).filter_by(cinema_id=a,movie_id=b,schedule_id=c)
    session=db.session.scalars(stmt)
    posts =  SessionSchema(many=True).dump(session)
    return posts

# retrieve single session data
@app_session.route("/sessions", methods=('GET', 'POST'))
@login_required
def get_sessions():
    all_sessions=[]
    for time in range(1,13):
        # all_sessions.append(time+'AM')
        all_sessions.append(str(time)+':00 PM')
    if request.method == 'POST':
        cinema_id = request.form['cinema_id']
        schedule_id = request.form['schedule_id']
        movie_id = request.form['movie_id']
        session_time=request.form['session_time']
        new_session= Session(
            schedule_id=schedule_id,
            cinema_id=cinema_id,
            movie_id=movie_id,
            session_time=session_time
        )
        # toast='schedule added !'    
        db.session.add(new_session)
        db.session.commit()
        return redirect(url_for('sessions.get_sessions'))
    cinemas=get_cinemas()
    movies=get_all_movies(cinemas[0]['id'])
    return render_template('cinema/all_sessions.html',all_sessions=all_sessions,cinemas=cinemas,movies=movies,user=current_user.username)


'''

# update single session
@app_session.route("/cinema/<int:cinema_id>/movie/<int:movie_id>/schedule/<int:schedule_id>/sessions/<int:session_id>",methods=['PUT'])
@jwt_required()
def update_session(session_id,movie_id,cinema_id):
    # check admin authorization
    admin_required()
     # check if session exist , error if not
    session_c = session_check(session_id)
    # get use input
    new_session= SessionSchema().load(request.form)
    # update schedule 
    session_c.session_time=new_session["session_time"]
    db.session.commit()
    return SessionSchema().dump(session_c), 201
'''


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
    # check if schedule exist
    schedule_c = session_check(schedule_id,cinema_id, movie_id,session_id)
    # delete movie
    db.session.delete(schedule_c)
    db.session.commit()
    return redirect(url_for('sessions.get_sessions'))
