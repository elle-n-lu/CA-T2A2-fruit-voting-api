from marshmallow import fields
from marshmallow.validate import Length
from pkg_init import db, ma
class Cinema(db.Model):
    __tablename__='cinemas'
    id=db.Column(db.Integer, primary_key=True)
    cinema_name= db.Column(db.String)
    registed_date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())
    
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"), nullable=False)
    
    movies=db.relationship("Movie", backref="cinemas", cascade="all, delete")
    orders=db.relationship("Order", backref="cinemas", cascade="all, delete")

class CinemaSchema(ma.Schema):
    cinema_name=fields.String(validate=Length(min=3))
    
    class Meta:
        fields=("id","cinema_name","movies","admin_id")
    
    movies= fields.List(fields.Nested("MovieSchema",exclude=('votes',"comments","schedules")))
    orders= fields.List(fields.Nested("OrderSchema",exclude=("cinema_id",)))
    
    