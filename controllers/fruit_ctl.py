
from flask_jwt_extended import  jwt_required
from sqlalchemy import exc
from flask import Blueprint, request
from pkg_init import db
from controllers.admin_ctl import admin_required
from models.fruit import FruitSchema, Fruit

app_fruit=Blueprint("fruit",__name__)

# create fruit kind only admin allowed
@app_fruit.route("/fruit",methods=['POST'])
@jwt_required()
def create_fruit():
    # check admin login
    admin=admin_required()
    # retrieve requested formdata
    fruit_name= FruitSchema().load(request.form)
    # add new fruit in db
    new_fruit= Fruit(
        fruit_name=fruit_name["fruit_name"],
        admin_id=admin.id
    )
    db.session.add(new_fruit)
    db.session.commit()
    return FruitSchema().dump(new_fruit), 201

# retrieve all fruit data
@app_fruit.route("/fruit",methods=['GET'])
def get_fruit():
    stmt=db.select(Fruit)
    fruit=db.session.scalars(stmt)
    return FruitSchema(many=True,exclude=['admin_id',]).dump(fruit)

# update single specie
@app_fruit.route("/fruit/<int:fruit_id>",methods=['PUT'])
@jwt_required()
def update_fruit(fruit_id):
    # check admin authentication
    admin_required()
    # check if fruit exist
    fruit_check=Fruit.query.filter_by(id=fruit_id).first()
    # get use input
    specie= FruitSchema().load(request.form)
    if not fruit_check:
        return {"error":"fruit not found"}
    # update fruit name
    fruit_check.fruit_name=specie.get("fruit_name", fruit_check.fruit_name)
    db.session.commit()
    return FruitSchema().dump(fruit_check), 201

# delete single fruit
@app_fruit.route("/fruit/<int:fruit_id>",methods=['DELETE'])
@jwt_required()
def delete_fruit(fruit_id):
    # check admin authentication
    admin_required()
    # check if fruit exist
    fruit_check=Fruit.query.filter_by(id=fruit_id).first()
    if not fruit_check:
        return {"error":"fruit not found"}
    # delete fruit
    db.session.delete(fruit_check)
    db.session.commit()
    return "fruit deleted"