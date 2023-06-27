
import re
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy import exc, select
from flask import Blueprint, request
from pkg_init import db
from controllers.user_ctl import login_required, owner_required
from models.votes import Vote, VoteSchema
from models.species import Specie

app_vote=Blueprint("vote",__name__,url_prefix='/species/<int:id>' )

# vote for one specie
@app_vote.route("/votes",methods=['POST'])
@jwt_required()
def create_vote(id):
    try:
        # convert input string to boolean
        z = lambda x: True if x.lower() =='true' else False
        # check user login
        user_id=login_required()
        # check if specie exist , error if not
        specie=Specie.query.filter_by(id=id).first()
        if not specie:
            return {'error':"specie not exist"}
        # avoid repetitive vote
        vote_check=Vote.query.filter_by(user_id=user_id, specie_id=id).first()
        if vote_check:
            return "already voted, you can only update it"
        # add use input in db
        vote= VoteSchema().load(request.form)
        new_vote= Vote(
            vote_status=z(vote['vote_status']),
            specie_id=id, 
            user_id=user_id
        )
        db.session.add(new_vote)
        db.session.commit()
        # return the new data 
        return VoteSchema().dump(new_vote), 201
    except KeyError:
        return {'error':"['vote_status']missing data required"}

# retrieve vote status
@app_vote.route("/votes/<int:vote_id>",methods=['GET'])
@jwt_required()   
def get_vote(id,vote_id):
    vote_check=Vote.query.filter_by(id=vote_id).first()
    return VoteSchema().dump(vote_check), 201

# update vote status to different or delete it
@app_vote.route("/votes/<int:vote_id>",methods=['PUT'])
@jwt_required()   
def update_vote(id,vote_id):
    # check if user already vote this specie
    vote_check=Vote.query.filter_by(id=vote_id).first()
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
    
        
    

