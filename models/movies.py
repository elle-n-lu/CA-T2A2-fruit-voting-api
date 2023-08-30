from pkg_init import db,ma
from marshmallow.validate import Length
from marshmallow import fields

class Movie(db.Model):
    __tablename__='movies'
    id=db.Column(db.Integer, primary_key=True)
    movie_name= db.Column(db.String)
    movie_poster=db.Column(db.String)
    introduction =db.Column(db.String)
    registed_date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())
    # m --- m 
    seats=db.relationship("Seat", secondary="movie_seat",back_populates="movies", cascade="all, delete")
    cinemas=db.relationship("Cinema", secondary="movie_seat",back_populates="movies", cascade="all, delete")

    cinema_id=db.Column(db.Integer, db.ForeignKey("cinemas.id"), nullable=True)
    
    # 1 -- n
    votes=db.relationship("Vote", backref="movies", cascade="all, delete")
    comments=db.relationship("Comment", backref="movies", cascade="all, delete")

    schedules=db.relationship("Schedule", backref="movies", cascade="all, delete")

    sessions = db.relationship("Session", back_populates="movie")


class MovieSchema(ma.Schema):
    movie_name=fields.String(validate=Length(min=3))
    
    class Meta:
        fields=("id","movie_name","movie_poster","introduction","comments","votes","schedules")
    
    votes=fields.List(fields.Nested("VoteSchema"))
    comments=fields.List(fields.Nested("CommentSchema"))
    schedules=fields.List(fields.Nested("ScheduleSchema",exclude=('sessions',)))