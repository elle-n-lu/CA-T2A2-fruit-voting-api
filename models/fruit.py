from marshmallow import fields
from pkg_init import db, ma
class Fruit(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    fruit_name= db.Column(db.String)
    date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())
    admin_id = db.Column(db.Integer, db.ForeignKey("admin.id"), nullable=False)
    
    species=db.relationship("Specie", backref="fruits", cascade="all, delete")

class FruitSchema(ma.Schema):
    class Meta:
        fields=("id","fruit_name","species","admin_id")
    
    species= fields.List(fields.Nested("SpecieSchema"))
    
    