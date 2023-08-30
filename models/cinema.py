from marshmallow import fields
from marshmallow.validate import Length
from pkg_init import db, ma
class Cinema(db.Model):
    __tablename__='cinemas'
    id=db.Column(db.Integer, primary_key=True)
    cinema_name= db.Column(db.String)
    registed_date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())
    
    movies=db.relationship("Movie", secondary="movie_seat", back_populates="cinemas",cascade="all, delete")
    seats=db.relationship("Seat", secondary="movie_seat",back_populates="cinemas", cascade="all, delete")
    
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"), nullable=False)
    

    orders=db.relationship("Order", backref="cinemas", cascade="all, delete")
    sessions = db.relationship("Session", back_populates="cinema")
    
class CinemaSchema(ma.Schema):
    cinema_name=fields.String(validate=Length(min=3))
    
    class Meta:
        fields=("id","cinema_name","movies","admin_id")
    
    movies= fields.List(fields.Nested("MovieSchema",exclude=('votes',"comments","schedules")))
    # orders= fields.List(fields.Nested("OrderSchema",exclude=("cinema_id",)))
    
    