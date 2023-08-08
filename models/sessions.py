from marshmallow import fields
from marshmallow.validate import Length
from pkg_init import db, ma

class Session(db.Model):
    __tablename__= 'sessions'
    id=db.Column(db.Integer, primary_key=True)
    session_time= db.Column(db.String)

    schedule_id = db.Column(db.Integer, db.ForeignKey("schedules.id"), nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False)
    cinema_id = db.Column(db.Integer, db.ForeignKey("cinemas.id"), nullable=False)

    seats=db.relationship("Seat", backref="sessions", cascade="all, delete")

class SessionSchema(ma.Schema):
    session_time=fields.String(validate=Length(min=2))
    
    class Meta:
        fields=("id","session_time","seats","schedule_id","movie_id","cinema_id")
    
    seats= fields.List(fields.Nested("SeatSchema"))
    
    