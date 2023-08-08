
from flask_jwt_extended import  jwt_required
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
from models.votes import Vote
from flask_login import login_user,login_required,current_user, logout_user


app_movie = Blueprint("movie", __name__)

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
in-use
'''
@app_movie.route("/ajax_movies/<int:a>", methods=['GET'])
def get_all_movies(a):
    stmt=db.select(Movie).filter_by(cinema_id=a)
    movie=db.session.scalars(stmt)
    posts =  MovieSchema(many=True).dump(movie)
    return posts

# retrive all movies data
@app_movie.route("/cinema/<int:id>/movies", methods=('GET', 'POST'))
@login_required
def get_movies(id):
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        introduction = request.form['introduction']
        new_movie = Movie(
            movie_name=movie_name,
            introduction = introduction,
            cinema_id=id
        )
        db.session.add(new_movie)
        db.session.commit()
        return redirect(url_for('movie.get_movies',id=id))
    posts = get_cinemas()
    stmt = db.select(Movie).filter_by(cinema_id=id)
    movies = db.session.scalars(stmt)
    movie =  MovieSchema(many=True, exclude=['votes','comments']).dump(movies)
    return render_template('cinema/main.html', movies=movie,posts=posts,user=current_user.username)

'''


# retrieve single movie data
@app_movie.route("/movies/<int:movie_id>", methods=['GET'])
def get_movie(id,movie_id):
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
        return MovieSchema().dump(movie)
'''


# update single movie
@app_movie.route("/cinema/<int:id>/movies/<int:movie_id>",methods=('GET', 'POST'))
@login_required
def update_movie(id,movie_id):
    # check admin authorization
    # admin_required()
    posts = get_cinemas()
    
    # check if movie exist , error if not
    movie_check=Movie.query.filter_by(id=movie_id).first()
    # get use input
    # movie= MovieSchema().load(request.form)
    if not movie_check:
        return {"error":"movie not found"}
    # update movie name
    if request.method == 'POST':
        movie_name = request.form['movie_name']
        introduction = request.form['introduction']
        movie_check.movie_name=movie_name
        movie_check.introduction=introduction
        db.session.commit()
        return redirect(url_for('movie.get_movies',id=id))
    movie_e= MovieSchema().dump(movie_check)
    return render_template('cinema/update.html', post=movie_e,posts=posts,user=current_user.username)



# delete single movie
@app_movie.route("/cinema/<int:id>/movies/delete/<int:movie_id>",methods=('POST',))
@login_required
def delete_movie(id,movie_id):
    # check admin authorization
    # admin_required()
    # check if movie exist
    movie_check=Movie.query.filter_by(id=movie_id,cinema_id=id).first()
    # if not movie_check:
    #     error = {"error":"movie not found"}
    #     flash(error)
    # delete movie
    db.session.delete(movie_check)
    db.session.commit()
    return redirect(url_for('movie.get_movies',id=id))
    # return "movie deleted"
