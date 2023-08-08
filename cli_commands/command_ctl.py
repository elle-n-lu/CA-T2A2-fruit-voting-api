
import os
from flask import Blueprint
from sqlalchemy.engine import Engine
from pkg_init import db, bcrypt
from models.admin import Admin
from models.users import User
from models.cinema import Cinema
from models.movies import Movie
from models.comments import Comment
from models.votes import Vote
from models.orders import Order
from models.schedules import Schedule
from models.sessions import Session
from models.seats import Seat
import sqlalchemy as sa

db_commands=Blueprint("db",__name__)

@db_commands.cli.command("drop")
def drop_db():
    engine = sa.create_engine(os.environ.get("DATABASE_URL"))

    insp = sa.inspect(engine)
    for table_entry in reversed(insp.get_sorted_table_and_fkc_names()):
        table_name = table_entry[0]
        if table_name:
            with engine.begin() as conn:
                conn.execute(sa.text(f'DROP TABLE "{table_name}"'))
#     db.metadata.drop_all(bind=Engine)
    print("tables dropped")

@db_commands.cli.command("create")
def create_db():
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
