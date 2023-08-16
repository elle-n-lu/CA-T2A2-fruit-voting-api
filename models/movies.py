from pkg_init import db,ma
from marshmallow.validate import Length
from marshmallow import fields

class Movie(db.Model):
    __tablename__='movies'
    id=db.Column(db.Integer, primary_key=True)
    movie_name= db.Column(db.String)
    introduction =db.Column(db.String)
    registed_date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())

    cinema_id=db.Column(db.Integer, db.ForeignKey("cinemas.id"), nullable=False)
    #add
    seat_id=db.Column(db.Integer, db.ForeignKey("seats.id"), nullable=False)

    votes=db.relationship("Vote", backref="movies", cascade="all, delete")
    comments=db.relationship("Comment", backref="movies", cascade="all, delete")

    schedules=db.relationship("Schedule", backref="movies", cascade="all, delete")



class MovieSchema(ma.Schema):
    movie_name=fields.String(validate=Length(min=3))
    
    class Meta:
        fields=("id","movie_name","introduction","comments","votes","schedules")
    
    votes=fields.List(fields.Nested("VoteSchema"))
    comments=fields.List(fields.Nested("CommentSchema"))
    schedules=fields.List(fields.Nested("ScheduleSchema"))