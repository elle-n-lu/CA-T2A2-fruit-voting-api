
from flask import Blueprint
from pkg_init import db, bcrypt
from models.admin import Admin
from models.users import User
from models.fruit import Fruit
from models.species import Specie
from models.comments import Comment
from models.votes import Vote

db_commands=Blueprint("db",__name__)

@db_commands.cli.command("create")
def create_db():
    db.drop_all()
    db.create_all()
    print("tables created")

@db_commands.cli.command("seed")
def seed_db():
    admin=Admin(
        username = "admin",
        email ="admin@email.com",
        password = bcrypt.generate_password_hash("admin").decode("utf-8"),
        admin=True
    )
    db.session.add(admin)
    db.session.commit()

    print("tables seeded")
