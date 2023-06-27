
from flask_jwt_extended import create_access_token, get_jwt_identity, jwt_required
from sqlalchemy import exc, select
from flask import Blueprint, request
from sqlalchemy import func
from marshmallow.exceptions import ValidationError
from controllers.user_ctl import owner_required
from pkg_init import db
from controllers.admin_ctl import admin_required
from models.species import SpecieSchema, Specie
from models.fruit import Fruit
from models.votes import Vote

app_specie = Blueprint("specie", __name__, url_prefix='/fruit/<int:id>')

# create a specie only admin allowed
@app_specie.route("/species", methods=['POST'])
@jwt_required()
def create_specie(id):
    try:
        # check admin login
        admin_required()
        # check if the fruit which the specie belong exist, error if not
        fruit=Fruit.query.filter_by(id=id).first()
        if not fruit:
            return {"error":"fruit not exist"}
        # add user data in db
        specie = SpecieSchema().load(request.form)
        new_specie = Specie(
            specie_name=specie['specie_name'],
            fruit_id=id
        )
        db.session.add(new_specie)
        db.session.commit()
        # return a value to show or use
        return SpecieSchema().dump(new_specie), 201
    except (KeyError,ValidationError):
        return {'error': "['specie_name'] data required"}

# retrive all species data
@app_specie.route("/species", methods=['GET'])
def get_species(id):
    
    stmt = db.select(Specie)
    species = db.session.scalars(stmt)
    return SpecieSchema(many=True).dump(species)

# retrieve single specie data
@app_specie.route("/species/<int:specie_id>", methods=['GET'])
def get_specie(id,specie_id):
    # check if specei exist, error if not
    specie=Specie.query.filter_by(id=specie_id).first()
    if not specie:
        return {'error':'specie not exist'}
    # if any user voted, check the votes count: up and down
    if specie.votes:
        stmt = (
                select(Vote.id, func.count(Vote.vote_status))
                .join_from(Specie, Vote)
                .group_by(Vote.vote_status,Specie.id,Vote.id)
                .having(Specie.id==specie.id, Vote.vote_status==True)
                )
        votesup=db.session.scalars(stmt).all()
        stmt_down = (
                select(Vote.id, func.count(Vote.vote_status))
                .join_from(Specie, Vote)
                .group_by(Vote.vote_status,Specie.id, Vote.id)
                .having(Specie.id==specie.id, Vote.vote_status==False)
                )
        votesdown=db.session.scalars(stmt_down).all()
        # return value for using
        return {'specie': SpecieSchema().dump(specie), "vote_up":len(votesup), "vote_down":len(votesdown)}
    else:
        return SpecieSchema().dump(specie)
    
# update single specie
@app_specie.route("/species/<int:specie_id>",methods=['PUT'])
@jwt_required()
def update_specie(id,specie_id):
    # check admin authorization
    admin_required()
    # check if specie exist , error if not
    specie_check=Specie.query.filter_by(id=specie_id).first()
    # get use input
    specie= SpecieSchema().load(request.form)
    if not specie_check:
        return {"error":"specie not found"}
    # update specie name
    specie_check.specie_name=specie["specie_name"]
    db.session.commit()
    return SpecieSchema().dump(specie_check), 201

# delete single specie
@app_specie.route("/species/<int:specie_id>",methods=['DELETE'])
@jwt_required()
def delete_specie(id,specie_id):
    # check admin authorization
    admin_required()

    # check if specie exist
    specie_check=Specie.query.filter_by(id=specie_id).first()
    if not specie_check:
        return {"error":"specie not found"}
    # delete specie
    db.session.delete(specie_check)
    db.session.commit()
    return "specie deleted"
