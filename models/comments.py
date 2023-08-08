from pkg_init import db, ma
from marshmallow import  fields, validates

class Comment(db.Model):
    __tablename__='comments'
    id=db.Column(db.Integer, primary_key=True)
    parent_comment_id = db.Column(db.Integer, default=None)
    message= db.Column(db.String)
    rated_mark = db.Column(db.String)
    registed_date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())

    movie_id=db.Column(db.Integer, db.ForeignKey("movies.id"), nullable=False)
    user_id=db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    

class CommentSchema(ma.Schema):
    class Meta:
        fields=("id","parent_comment_id","message", "movie","user_id")
    
    movie=fields.Nested("MovieSchema")
    
    @validates('parent_comment_id')
    def validate_parent_comment_id(self, parent_comment_id):
        parent_comment_check= Comment.query.filter_by(id=parent_comment_id).first()
        comment=Comment.query.filter_by(parent_comment_id=parent_comment_id).first()
        if not parent_comment_check:
            db.session.delete(comment)
            db.session.commit()