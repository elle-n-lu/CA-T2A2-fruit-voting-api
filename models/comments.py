from pkg_init import db, ma
from marshmallow import fields

class Comment(db.Model):
    __tablename__='comments'
    id=db.Column(db.Integer, primary_key=True)
    parent_comment_id = db.Column(db.Integer, default=None)
    message= db.Column(db.String)
    date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())

    specie_id=db.Column(db.Integer, db.ForeignKey("species.id"), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    

class CommentSchema(ma.Schema):
    class Meta:
        fields=("id","parent_comment_id","message", "specie","user_id")
    
    specie=fields.Nested("SpecieSchema")