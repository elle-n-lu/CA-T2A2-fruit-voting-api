from pkg_init import db, ma
from marshmallow.validate import Length, Regexp
from marshmallow import fields
class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(),nullable=False)
    email = db.Column(db.String(),nullable=False, unique=True)
    password = db.Column(db.String(),nullable=False,)
    date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())


    votes=db.relationship("Vote", backref="users", cascade="all, delete")
    comments=db.relationship("Comment", backref="users", cascade="all, delete")

class UserSchema(ma.Schema):
    username=fields.String(validate=Length(min=3))
    password=fields.String( validate=Length(min=8))
    email=fields.String(validate=Regexp('^[a-zA-Z][a-zA-Z0-9-_.]*@[a-zA-Z]+.[a-zA-Z]{1,3}$'))

    class Meta:
        fields=("id","username","email", "password", "votes","comments")

    votes= fields.List(fields.Nested("VoteSchema", exclude=['user_id',]))
    comments= fields.List(fields.Nested("CommentSchema", exclude=['user_id',]))
    