from models.movies import Movie
from models.movie_seat import Movie_Seat
from flask_jwt_extended import  jwt_required
from flask import Blueprint, flash, redirect, render_template, request, url_for
from controllers.cinema_ctl import get_cinemas

from flask_login import login_required, current_user
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

def get_seat_numbers():
    seats = get_seats()
    totalseatnumbers=[]
    totalseatnumbers.append('')
    for i in seats:
        totalseatnumbers.append(i['seat_number'])
    return sorted(list( dict.fromkeys(totalseatnumbers) ))

@app_seat.route("/seats_add",methods=( 'POST',) )
def add_seat():
    cinema_id = request.form['cinema_id']
    seat_number = request.form['seat_number']
    new_seat = Seat(
        seat_number=seat_number,
        cinema_id = cinema_id
    )
    db.session.add(new_seat)
    db.session.commit()
    return redirect(url_for('seats.create_total_seat',))

@app_seat.route("/seats/filte",methods=( 'POST',) )
@login_required
def filter_seat():
    cinemas = get_cinemas()
    cinemas.insert(0, '')
    seatnumbers = get_seat_numbers()
    totalseats = get_seats()

    cinema_id = request.form['cinema_id']
    seat_number = request.form['seat_number']
    if seat_number == ''and cinema_id !='' :
        stmt=db.select(Seat).filter_by(cinema_id=cinema_id)
        session=db.session.scalars(stmt)
        seats =  SeatSchema(many=True).dump(session)
        return render_template('cinema/seats.html', seats=seats,seatnumbers= seatnumbers, cinemas=cinemas)
    if cinema_id == '' and seat_number !='':
        stmt=db.select(Seat).filter_by(seat_number=seat_number)
        session=db.session.scalars(stmt)
        seats =  SeatSchema(many=True).dump(session)
        return render_template('cinema/seats.html', seats=seats,seatnumbers= seatnumbers, cinemas=cinemas)
    if cinema_id == '' and seat_number=='':
        return render_template('cinema/seats.html', seats=totalseats,seatnumbers= seatnumbers, cinemas=cinemas)
    stmt=db.select(Seat).filter_by(cinema_id=cinema_id, seat_number=seat_number)
    session=db.session.scalars(stmt)
    seats =  SeatSchema(many=True).dump(session)
    return render_template('cinema/seats.html', seats=seats,seatnumbers= seatnumbers, cinemas=cinemas,user=current_user.username)

@app_seat.route("/seats",  methods=('GET', 'POST'))
@login_required
def create_total_seat():
    cinemas = get_cinemas()
    cinemas.insert(0, '')

    totalseats = get_seats()
    seatnumbers = get_seat_numbers()
    return render_template('cinema/seats.html',user=current_user.username, seats=totalseats,seatnumbers= seatnumbers, cinemas=cinemas)

@app_seat.route("/ajax_seats/<int:a>", methods=['GET'])
def get_all_seats_by_cinema(a):
    stmt=db.select(Seat).filter_by(cinema_id=a)
    session=db.session.scalars(stmt)
    seats =  SeatSchema(many=True).dump(session)
    return seats

@app_seat.route("/seats/destribute_movie",methods=('GET','POST'))
@login_required
def add_playing_movie():
    cinemas = get_cinemas()
    totalseats = get_all_seats_by_cinema(cinemas[0]['id'])

    if request.method == 'POST':
        cinema_id = request.form['cinema_id']
        seat_id = request.form['seat_id']
        movie_id=request.form['movie_id']
        # add movie_id for seat room in cinema_id
        # alter table 'movies' insert seat_id =seat_id where movie_id=movie_id, cinema_id=cinema_id
        movie_check=Movie_Seat.query.filter_by(cinema_id=cinema_id, seat_id=seat_id,movie_id=movie_id).first()
        if movie_check:
            flash('movie already exist!')
        new_movie_seat = Movie_Seat(
            movie_id = movie_id,
            seat_id=seat_id,
            cinema_id = cinema_id
        )
        db.session.add(new_movie_seat)
        db.session.commit()
        return redirect(url_for('seats.add_playing_movie'))
    
    return render_template('cinema/seat_addmovie.html',cinemas=cinemas, seats= totalseats, user=current_user.username)

@app_seat.route("/cinemas/<int:cinema_id>/seats/<int:id>/delete",methods=('GET','POST'))
@login_required
def delete_a_seat(cinema_id,id):
    if request.method == 'POST':
        seat_check=Seat.query.filter_by(id=id,cinema_id=cinema_id).first()
        db.session.delete(seat_check)
        db.session.commit()
        return redirect(url_for('seats.create_total_seat'))
    return render_template('cinema/update_seat.html', user=current_user.username)




