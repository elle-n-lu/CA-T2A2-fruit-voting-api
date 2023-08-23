
from app import set_up
from pkg_init import db, bcrypt
from models.users import User

app = set_up()

if __name__ == "__main__":
    with app.app_context():
        db.drop_all()
        db.create_all()
        admin = User(
            username="admin",
            email="admin@email.com",
            password=bcrypt.generate_password_hash("admin").decode("utf-8"),
            admin=True,
        )
        db.session.add(admin)
        db.session.commit()

        
        

        app.run(debug=True)