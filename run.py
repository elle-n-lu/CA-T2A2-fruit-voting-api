
import os
from app import setup
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
from models.movie_seat import Movie_Seat
import sqlalchemy as sa


app = setup()

if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        db.create_all()
        admin=Admin(
            username = "admin",
            email ="admin@email.com",
            password = bcrypt.generate_password_hash("admin").decode("utf-8"),
            admin=True
        )
        db.session.add(admin)
        db.session.commit()
        
        app.run(debug=True)