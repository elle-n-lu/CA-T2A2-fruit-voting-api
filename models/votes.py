from pkg_init import db, ma
from marshmallow import fields

class Vote(db.Model):
    __tablename__='votes'
    id=db.Column(db.Integer, primary_key=True)
    vote_status= db.Column(db.Boolean, default=None)
    registed_date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())
    
    movie_id=db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    
class VoteSchema(ma.Schema):
    vote_status=fields.String(required=True)

    class Meta:
        fields=("id","vote_status","movie","user_id")
    
    movie=fields.Nested("MovieSchema")