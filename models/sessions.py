from marshmallow import fields
from marshmallow.validate import Length
from pkg_init import db, ma

class Session(db.Model):
    __tablename__= 'sessions'
    id=db.Column(db.Integer, primary_key=True)
    session_time= db.Column(db.String)
    price=db.Column(db.Integer)

    # add later
    seat_id = db.Column(db.Integer, db.ForeignKey("seats.id"), nullable=False)

    schedule_id = db.Column(db.Integer, db.ForeignKey("schedules.id"), nullable=False)
    schedule=db.relationship("Schedule", back_populates="sessions")


    cinema_id = db.Column(db.Integer, db.ForeignKey("cinemas.id"), nullable=False)
    cinema=db.relationship("Cinema", back_populates="sessions")

    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False)
    movie=db.relationship("Movie", back_populates="sessions")

    orders=db.relationship("Order", back_populates="session")


class SessionSchema(ma.Schema):
    session_time=fields.String(validate=Length(min=2))
    
    class Meta:
        fields=("id","session_time","price","schedule_id","movie_id","cinema_id","movie","cinema","schedule")
    
    movie =  fields.Nested("MovieSchema",exclude=("comments","votes","schedules")) 
    cinema =  fields.Nested("CinemaSchema",exclude=("movies",)) 
    schedule =  fields.Nested("ScheduleSchema",exclude=("cinema_id","movie_id","seat_id")) 
    
    