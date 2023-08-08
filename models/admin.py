from marshmallow import fields
from flask_login import UserMixin
from pkg_init import db, ma

class Admin(UserMixin,db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(),nullable=False)
    email = db.Column(db.String(),nullable=False, unique=True)
    password = db.Column(db.String(),nullable=False,)
    admin = db.Column(db.Boolean(), default=False)
    date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())

    cinemas=db.relationship("Cinema", backref="admin", cascade="all, delete")
    orders=db.relationship("Order", backref="admin", cascade="all, delete")

class AdminSchema(ma.Schema):
    class Meta:
        fields=("id","username","email","password","cinemas","orders")
    
    cinemas= fields.List(fields.Nested("CinemaSchema"))
    orders= fields.List(fields.Nested("OrderSchema"))