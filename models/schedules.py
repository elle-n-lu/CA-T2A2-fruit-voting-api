from marshmallow import fields
from marshmallow.validate import Length
from pkg_init import db, ma
class Schedule(db.Model):
    __tablename__='schedules'
    id=db.Column(db.Integer, primary_key=True)
    schedule_date= db.Column(db.DateTime(timezone=True))

    movie_id = db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False)
    cinema_id = db.Column(db.Integer, db.ForeignKey("cinemas.id"), nullable=False)
    #add
    seat_id = db.Column(db.Integer, db.ForeignKey("seats.id"), nullable=False)

    sessions=db.relationship("Session", backref="schedules", cascade="all, delete")

class ScheduleSchema(ma.Schema):
    schedule_date=fields.String(validate=Length(min=2))
    
    class Meta:
        fields=("id","schedule_date","sessions","movie_id","cinema_id","seat_id")
    
    sessions= fields.List(fields.Nested("SessionSchema"))
    
    