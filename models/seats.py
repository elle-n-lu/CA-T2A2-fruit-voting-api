from marshmallow import fields
from marshmallow.validate import Length
from pkg_init import db, ma

class Seat(db.Model):
    __tablename__= 'seats'
    id=db.Column(db.Integer, primary_key=True)
    seat_number= db.Column(db.String)
    # seat_status = db.Column(db.Boolean(), default=False)
    
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)
    
class SeatSchema(ma.Schema):
    
    class Meta:
        fields=("id","seat_number",)
    
    
    