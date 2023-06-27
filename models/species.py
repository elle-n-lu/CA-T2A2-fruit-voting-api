from pkg_init import db,ma
from marshmallow import fields

class Specie(db.Model):
    __tablename__='species'
    id=db.Column(db.Integer, primary_key=True)
    specie_name= db.Column(db.String)
    date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())
    
    fruit_id=db.Column(db.Integer, db.ForeignKey("fruit.id"), nullable=False)

    votes=db.relationship("Vote", backref="species", cascade="all, delete")
    comments=db.relationship("Comment", backref="species", cascade="all, delete")

class SpecieSchema(ma.Schema):
    class Meta:
        fields=("id","specie_name","comments","votes")
    
    votes=fields.List(fields.Nested("VoteSchema"))
    comments=fields.List(fields.Nested("CommentSchema"))