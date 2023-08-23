
from controllers.user_ctl import user_login_required
from models.orders import Order
from models.movie_seat import Movie_Seat,MovieSeatSchema
from models.sessions import Session, SessionSchema
from controllers.seat_ctl import get_all_seats_by_cinema
from flask_jwt_extended import  get_jwt_identity, jwt_required
from controllers.order_ctl import get_order_ss
from controllers.cinema_ctl import get_cinemas
from models.cinema import CinemaSchema
from sqlalchemy import exc, select
from flask import Blueprint, flash, redirect, render_template, request, url_for
from sqlalchemy import func
from marshmallow.exceptions import ValidationError
from controllers.user_ctl import owner_required
from pkg_init import db
from controllers.admin_ctl import admin_required
from models.movies import MovieSchema, Movie
from models.cinema import Cinema
from models.votes import Vote, VoteSchema
from flask_login import login_user,login_required,current_user, logout_user
from sqlalchemy.sql import exists

app_movie = Blueprint("movie", __name__)
'''

# create a movie only admin allowed
@app_movie.route("/movies/all", methods=['POST'])
@jwt_required()
def create_movie(id):
    # check admin login
    admin_required()
    # check if the cinema which the movie belong exist, error if not
    cinema=Cinema.query.filter_by(id=id).first()
    if not cinema:
        return {"error":"cinema not exist"}
    # add user data in db
    movie = MovieSchema().load(request.form)
    new_movie = Movie(
        movie_name=movie['movie_name'],
        introduction = movie['introduction'],
        cinema_id=id
    )
    db.session.add(new_movie)
    db.session.commit()
    # return a value to show or use
    return MovieSchema().dump(new_movie), 201
'''

'''
in-use
'''
@app_movie.route("/ajax_movies_bind_seat", methods=['GET'])
def filter_movie_notbind_seat():
    stmt=db.select(Movie)
    movie=db.session.scalars(stmt)
    posts =  MovieSchema(many=True).dump(movie)
    return posts

@app_movie.route("/allmovies", methods=('GET', 'POST'))
def all_movies():
    posts = filter_movie_notbind_seat()
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        movie_poster = request.form['movie_poster']
        introduction = request.form['introduction']
        new_movie = Movie(
            movie_poster=movie_poster,
            movie_name=movie_name,
            introduction = introduction,
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('movie.all_movies'))
    return render_template('cinema/main.html',posts=posts,user=current_user.username)

'''
suppose to filter the movie not in the select room in selected cinema
'''
# @app_movie.route("/ajax_movies_bind_seat/<int:a>/<int:b>", methods=['GET'])
# def filter_movie_notbind_seat(a,b):
#     stmt=exists().where(Movie.seat_id==b)
#     movie=db.session.query(Movie).filter_by(cinema_id=a).filter(~stmt)
#     posts =  MovieSchema(many=True).dump(movie)
#     print('movi', movie)
#     return posts

@app_movie.route("/ajax_movies_cinema/<int:a>", methods=['GET'])
def get_all_movies_fromcinam(a):
    stmt=db.select(Movie).filter_by(cinema_id=a)
    movie=db.session.scalars(stmt)
    posts =  MovieSchema(many=True).dump(movie)
    return posts

@app_movie.route("/ajax_movies/<int:a>/<int:b>", methods=['GET'])
def get_all_movies(a,b):
    stmt=db.select(Movie_Seat).filter_by(seat_id=a, cinema_id=b)
    movie_id=db.session.scalars(stmt)
    posts =  MovieSeatSchema(many=True).dump(movie_id)
    movies=[]
    for i in posts:
        movie_=Movie.query.filter_by(id=i['movie_id']).first()
        movies_ =  MovieSchema().dump(movie_)
        movies.append(movies_)
    return movies

# retrive all movies data
'''
@app_movie.route("/cinema/<int:id>/movies", methods=('GET', 'POST'))
@login_required
def get_movies(id):
    seats = get_all_seats_by_cinema(id)
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        introduction = request.form['introduction']
        new_movie = Movie(
            movie_name=movie_name,
            introduction = introduction,
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('movie.get_movies',id=id))
    posts = get_cinemas()
    stmt = db.select(Movie)
    movies = db.session.scalars(stmt)
    movie =  MovieSchema(many=True, exclude=['votes','comments']).dump(movies)
    return render_template('cinema/main.html',seats=seats, movies=movie,posts=posts,user=current_user.username)
'''

@app_movie.route("/singlemovie/<int:movie_id>/<int:user_id>", methods=['GET'])
def get_usert_vote_status(movie_id, user_id):
    vote = Vote.query.filter_by(movie_id=movie_id, user_id=user_id).first()
    if vote:
        vote_=VoteSchema().dump(vote)
        return {'vote_id':vote_['id']}
    else: 
        return {'vote_id':""}

# retrieve single movie data
@app_movie.route("/singlemovie/<int:movie_id>", methods=['GET'])
def get_single_movie(movie_id):
    # check if movie exist, error if not
    
    movie=Movie.query.filter_by(id=movie_id).first()
    if not movie:
        return {'error':'movie not exist'}
    # if any user voted, check the votes count: up and down
    if movie.votes:
        stmt = (
                select(Vote.id, func.count(Vote.vote_status))
                .join_from(Movie, Vote)
                .group_by(Vote.vote_status,Movie.id,Vote.id)
                .having(Movie.id==movie.id, Vote.vote_status==True)
                )
        votesup=db.session.scalars(stmt).all()
        stmt_down = (
                select(Vote.id, func.count(Vote.vote_status))
                .join_from(Movie, Vote)
                .group_by(Vote.vote_status,Movie.id, Vote.id)
                .having(Movie.id==movie.id, Vote.vote_status==False)
                )
        votesdown=db.session.scalars(stmt_down).all()
        # return value for using
        return {'movie': MovieSchema().dump(movie), "vote_up":len(votesup), "vote_down":len(votesdown)}
    else:
        return {"movie":MovieSchema(exclude=("schedules",)).dump(movie),"vote_up":None, "vote_down":None}



# update single movie
@app_movie.route("/movies/<int:movie_id>",methods=('GET', 'POST'))
@login_required
def update_movie(movie_id):
    # check admin authorization
    # admin_required()

    # posts = get_cinemas()
    # check if movie exist , error if not
    movie_check=Movie.query.filter_by(id=movie_id).first()
    # get use input
    # movie= MovieSchema().load(request.form)
    if not movie_check:
        return {"error":"movie not found"}
    # update movie name
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        movie_poster=request.form['movie_poster']
        introduction = request.form['introduction']

        movie_check.movie_name=movie_name
        movie_check.movie_poster=movie_poster
        movie_check.introduction=introduction
        db.session.commit()
        return redirect(url_for('movie.all_movies'))
    movie_e= MovieSchema().dump(movie_check)
    return render_template('cinema/update.html', post=movie_e,user=current_user.username)



# delete single movie
@app_movie.route("/movies/delete/<int:movie_id>",methods=('POST',))
@login_required
def delete_movie(movie_id):
    # check admin authorization
    # admin_required()

    # check if movie exist
    movie_select=Movie.query.filter_by(id=movie_id).first()
    print('sel', movie_select)
    # check the session for the movie
    session_check=Session.query.filter_by(movie_id=movie_id).first()
    if session_check:
        session_e= SessionSchema().dump(session_check)
        # check if ordered the movie yet
        order_check=Order.query.filter_by(session_id=session_e['id']).first()
        if order_check:
            error = "movie can't be deleted because already booked to play"
            flash(error)
            return redirect(url_for('movie.all_movies'))

    # delete movie
    db.session.delete(movie_select)
    db.session.commit()
    return redirect(url_for('movie.all_movies'))
    # return "movie deleted"
