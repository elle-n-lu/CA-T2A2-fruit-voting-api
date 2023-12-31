from models.cinema import Cinema
from marshmallow import fields
from sqlalchemy.dialects.postgresql import JSON
from marshmallow.validate import Length
from pkg_init import db, ma

class Seat(db.Model):
    __tablename__= 'seats'
    id=db.Column(db.Integer, primary_key=True)
    seat_number= db.Column(db.String)
    # seat_status = db.Column(db.Boolean(), default=False)
    
    # add
    cinema_id = db.Column(db.Integer, db.ForeignKey("cinemas.id"), nullable=False)

    movies=db.relationship("Movie", secondary="movie_seat",back_populates="seats", cascade="all, delete")
    cinemas=db.relationship("Cinema", secondary="movie_seat",back_populates="seats", cascade="all, delete")
    
class SeatSchema(ma.Schema):
    
    class Meta:
        fields=("id","seat_number","cinema_id")
    
    # movies= fields.List(fields.Nested("MovieSchema",exclude=('votes',"comments","schedules")))

    
    
    