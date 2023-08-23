
import re
from flask_jwt_extended import jwt_required
from flask import Blueprint, request
from pkg_init import db
from controllers.user_ctl import user_login_required, owner_required
from models.votes import Vote, VoteSchema
from models.movies import Movie

app_vote=Blueprint("vote",__name__,url_prefix='/movies/<int:id>' )


# vote for one movie
@app_vote.route("/votes",methods=['POST'])
@jwt_required()
def create_vote(id):
    # convert input string to boolean
    z = lambda x: True if x.lower() =='true' else False
    # check user login
    user_id=user_login_required()
    # check if movie exist , error if not
    movie=Movie.query.filter_by(id=id).first()
    if not movie:
        return {'error':"movie not exist"}
    # avoid repetitive vote
    vote_check=Vote.query.filter_by(user_id=user_id, movie_id=id).first()
    if vote_check:
        return "already voted, you can only update it"
    # add use input in db
    vote= VoteSchema().load(request.form)
    new_vote= Vote(
        vote_status=z(vote['vote_status']),
        movie_id=id, 
        user_id=user_id
    )
    db.session.add(new_vote)
    db.session.commit()
    # return the new data 
    return VoteSchema().dump(new_vote), 201

# retrieve vote status
@app_vote.route("/votes",methods=['GET'])
def get_vote(id):
    vote_check=Vote.query.all()
    return VoteSchema(many=True).dump(vote_check), 201


# update vote status to different or delete it
@app_vote.route("/votes/<int:vote_id>",methods=['PUT'])
@jwt_required()   
def update_vote(id,vote_id):
    # check if user already vote this movie
    vote_check=Vote.query.filter_by(movie_id=id, id=vote_id).first()
    # get use input
    vote= VoteSchema().load(request.form)
    # if voted but user try to vote again,check vote status if not same then update
    if not vote_check:
        return {"error":"not voted, is it necessary to handle this error??"}
    # check only owner can update
    owner_required(vote_check.user_id)

    # if vote status different then change, otherwise delete if there already a status
    z = lambda x: True if x.lower() =='true' else False

    if vote_check.vote_status != z(vote['vote_status']):
        vote_check.vote_status= z(vote['vote_status'])
        db.session.commit()
        return VoteSchema().dump(vote_check), 201
    else:
        db.session.delete(vote_check)
        db.session.commit()
        return "vote cancelled"
    
        
    

