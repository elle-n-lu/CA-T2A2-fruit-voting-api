
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy import exc, select
from flask import Blueprint, request, jsonify
from marshmallow.exceptions import ValidationError
from pkg_init import db
from controllers.user_ctl import login_required, owner_required
from models.comments import Comment, CommentSchema

app_comment=Blueprint("comment",__name__,url_prefix='/species/<int:id>' )

# create comment authentication required
@app_comment.route("/comments",methods=['POST'])
@jwt_required()
def create_comment(id):
    try:
        # login check
        user_id=login_required()
        # retrieve requested formdata
        comment= CommentSchema().load(request.form)
        # check if the comment is to reply, if so there is a parent_comment_id
        parent_comment_id = comment['parent_comment_id']
        # check if the parent comment exist, error if not
        if parent_comment_id:
            commen=Comment.query.filter_by(id=parent_comment_id).first()
            if not commen:
                return {'error':"can't reply, comment not exist"}
        # add new comment in db
        new_message= Comment(
            message=comment['message'],
            parent_comment_id=parent_comment_id,
            specie_id=id, 
            user_id=user_id
        )
        db.session.add(new_message)
        db.session.commit()
        # return data for using
        return CommentSchema().dump(new_message), 201
    except (KeyError,ValidationError):
        return {'error':"['message'] data required"}

# retrieve all parent comment
@app_comment.route("/comments",methods=['GET'])
def get_comments(id):
    comment=Comment.query.filter_by(parent_comment_id=None)
    comments = CommentSchema(many=True).dump(comment)
    return comments

# retrieve children comment belong to one parent comment
@app_comment.route("/comments/<int:parent_comment_id>",methods=['GET'])
def get_comment(id, parent_comment_id):
    comment=Comment.query.filter_by(parent_comment_id=parent_comment_id)
    comments = CommentSchema(many=True).dump(comment)
    return comments

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
    if not comment_check:
        return {"error":"comment not found"}
    # check owner authentication
    owner_required(comment_check.user_id)

    db.session.delete(comment_check)
    db.session.commit()
    return "comment deleted"







    

