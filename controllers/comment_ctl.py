
from flask_jwt_extended import  jwt_required
from flask import Blueprint, request
from pkg_init import db
from controllers.user_ctl import user_login_required, owner_required
from models.comments import Comment, CommentSchema

app_comment=Blueprint("comment",__name__,url_prefix='/movies/<int:id>' )

# create comment authentication required
@app_comment.route("/comments",methods=['POST'])
@jwt_required()
def create_comment(id):
    # login check
    user_id=user_login_required()
    # retrieve requested formdata
    comment= CommentSchema().load(request.form)
    new_message= Comment(
        message=comment['message'],
        movie_id=id, 
        user_id=user_id
    )
    db.session.add(new_message)
    db.session.commit()
    # return data for using
    return CommentSchema().dump(new_message), 201

# reply comment authentication required
@app_comment.route("/comments/<int:parent_comment_id>",methods=['POST'])
@jwt_required()
def reply_comment(id,parent_comment_id):
    # login check
    user_id=user_login_required()
    # retrieve requested formdata
    comment= CommentSchema().load(request.form)
    # check if the parent comment exist, error if not
    commen=Comment.query.filter_by(id=parent_comment_id).first()
    if not commen:
        return {'error':"can't reply, comment not exist"}
    # add new comment in db
    new_message= Comment(
        message=comment['message'],
        parent_comment_id=parent_comment_id,
        movie_id=id, 
        user_id=user_id
    )
    db.session.add(new_message)
    db.session.commit()
    # return data for using
    return CommentSchema().dump(new_message), 201

# retrieve all parent comment
@app_comment.route("/comments",methods=['GET'])
def get_comments(id):
    comment=Comment.query.filter_by(parent_comment_id=None)
    comments = CommentSchema(many=True).dump(comment)
    return comments

# retrieve children comment belong to one parent comment
@app_comment.route("/comments/<int:parent_comment_id>",methods=['GET'])
def get_comment(id, parent_comment_id):
    parent_comment_check= Comment.query.filter_by(id=parent_comment_id).first()
    comment=Comment.query.filter_by(parent_comment_id=parent_comment_id).first()
    print(parent_comment_check,comment)
    if comment:
        if not parent_comment_check:
            db.session.delete(comment)
            db.session.commit()
            return 'comment not available'
        else:
            comments = CommentSchema(many=True).dump(Comment.query.filter_by(parent_comment_id=parent_comment_id))
            return comments
    else:
        return 'no such comment'

# update single comment
@app_comment.route("/comments/<int:comment_id>",methods=['PUT'])
@jwt_required()
def update_comment(id,comment_id):
    # check comment if exist, error if not
    comment_check=Comment.query.filter_by(id=comment_id).first()
    # get use input
    comment= CommentSchema().load(request.form)
    if not comment_check:
        return {"error":"comment not found"}
    # check only owner can update
    owner_required(comment_check.user_id)
    # update comment 
    comment_check.message=comment["message"]
    db.session.commit()
    return CommentSchema().dump(comment_check), 201

# delete single comment
@app_comment.route("/comments/<int:comment_id>",methods=['DELETE'])
@jwt_required()
def delete_comment(id,comment_id):
    comment_check=Comment.query.filter_by(id=comment_id).first()
    child_comment_check=Comment.query.filter_by(parent_comment_id=comment_id).first()
    if not comment_check :
        return {"error":"comment not found"}
    # check owner authentication
    owner_required(comment_check.user_id)

    # delete comment and its replied comments
    db.session.delete(comment_check)
    db.session.delete(child_comment_check)
    db.session.commit()
    return "comment deleted"







    

