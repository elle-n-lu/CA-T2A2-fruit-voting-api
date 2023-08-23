from marshmallow import fields
from marshmallow.validate import Length
from pkg_init import db, ma

class Movie_Seat(db.Model):
    __tablename__='movie_seat'
    cinema_id=db.Column(db.Integer,db.ForeignKey("cinemas.id"), primary_key=True)
    seat_id=db.Column(db.Integer,db.ForeignKey("seats.id"), primary_key=True)
    movie_id=db.Column(db.Integer,  db.ForeignKey("movies.id"), primary_key=True)


class MovieSeatSchema(ma.Schema):
    
    class Meta:
        fields=("movie_id","seat_id","cinema_id")