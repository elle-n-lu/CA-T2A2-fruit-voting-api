
import os
from app import setup
from pkg_init import db, bcrypt
from models.users import User
import sqlalchemy as sa


app = setup()

if __name__ == "__main__":
    with app.app_context():
        # db.drop_all()
        engine = sa.create_engine(os.environ.get("DATABASE_URL"))

        insp = sa.inspect(engine)
        for table_entry in reversed(insp.get_sorted_table_and_fkc_names()):
            table_name = table_entry[0]
            if table_name:
                with engine.begin() as conn:
                    conn.execute(sa.text(f'DROP TABLE IF EXISTS "{table_name}" CASCADE'))
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