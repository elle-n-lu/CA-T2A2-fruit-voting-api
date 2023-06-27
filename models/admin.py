from marshmallow import fields
from pkg_init import db, ma
class Admin(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(),nullable=False)
    email = db.Column(db.String(),nullable=False, unique=True)
    password = db.Column(db.String(),nullable=False,)
    admin = db.Column(db.Boolean(), default=False)
    date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())

    fruit=db.relationship("Fruit", backref="admin", cascade="all, delete")

class AdminSchema(ma.Schema):
    class Meta:
        fields=("id","username","email","password","fruit")
    
    fruit= fields.List(fields.Nested("FruitSchema"))