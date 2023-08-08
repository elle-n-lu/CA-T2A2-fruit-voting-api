from marshmallow import fields
from marshmallow.validate import Length
from pkg_init import db, ma

class Order(db.Model):
    __tablename__= 'orders'
    id=db.Column(db.Integer, primary_key=True)
    movie_name = db.Column(db.String)
    schedule = db.Column(db.DateTime(timezone=True))
    session = db.Column(db.String)
    seat = db.Column(db.String)
    registed_date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())

    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    cinema_id = db.Column(db.Integer, db.ForeignKey("cinemas.id"), nullable=False)
    
class OrderSchema(ma.Schema):
    
    class Meta:
        fields=("id","movie_name","schedule","session","seat","user_id","cinema_id",)
    
    
    