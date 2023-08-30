from marshmallow import fields
from marshmallow.validate import Length
from pkg_init import db, ma

class Order(db.Model):
    __tablename__= 'orders'
    id=db.Column(db.Integer, primary_key=True)
    
    seat = db.Column(db.String)
    total_price = db.Column(db.Integer)
    registed_date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())


    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"), nullable=False)
    cinema_id = db.Column(db.Integer, db.ForeignKey("cinemas.id"), nullable=False)
    # add
    session_id = db.Column(db.Integer, db.ForeignKey("sessions.id"), nullable=False)
    session = db.relationship("Session", back_populates="orders")

    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="orders")
    
class OrderSchema(ma.Schema):
    user =  fields.Nested("UserSchema",exclude=('comments','votes')) 
    session =  fields.Nested("SessionSchema") 
    class Meta:
        fields=("id","seat","user","session","total_price","registed_date")
    
    
    
    