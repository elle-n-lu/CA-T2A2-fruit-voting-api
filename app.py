import os
from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_login import current_user,login_required
from marshmallow.exceptions import ValidationError
from werkzeug.exceptions import BadRequest
from sqlalchemy import exc
from psycopg2.errors import UniqueViolation
from pkg_init import db,ma, bcrypt, jwt, mail, login_manager
from cli_commands.command_ctl import db_commands
from controllers.admin_ctl import app_admin
from controllers.user_ctl import app_user
from controllers.cinema_ctl import app_cinema
from controllers.movie_ctl import app_movie
from controllers.comment_ctl import app_comment
from controllers.vote_ctl import app_vote
from controllers.schedule_ctl import app_schedule
from controllers.session_ctl import app_session
from controllers.seat_ctl import app_seat
from controllers.order_ctl import app_order
from models.admin import Admin

controllers=[app_admin, app_user, app_cinema, app_movie, app_vote, 
             app_comment,app_schedule,app_session,
             app_seat,app_order 
            ]

def setup():
    app=Flask(__name__)
    app.config.from_object("config.app_config")
    app.secret_key =  os.environ.get("SESSION_SECRET_KEY")
    CORS(app,origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000"
        ],supports_credentials=True)

    login_manager.login_view='admin.admin_login'
    login_manager.init_app(app)
    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    mail.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return Admin.query.get(user_id)

    @app.route("/",methods=['GET'])
    def say_hello():
        return 'hi there'
    
    @app.route("/index",methods=['GET'])
    @login_required
    def index_page():
        return render_template('cinema/index.html', user=current_user.username)

    
    app.register_blueprint(db_commands)
    for controller in controllers:
        app.register_blueprint(controller)

    @app.errorhandler(401)
    def unauthorised(err):
        return {"error":"You are not authorised"}, 401
    
    @app.errorhandler(BadRequest)
    def default_error(e):
        return jsonify({'error': e.description}), 400

    @app.errorhandler(KeyError)
    def bad_request(err):
        return jsonify({'error': f'The field {err} is required'}), 400

    @app.errorhandler(ValidationError)
    def bad_request(err):
        return {'error':err.__dict__["messages"]}, 400

    @app.errorhandler(404)
    def resource_not_found(e):
        return {'error':'page not found'}, 404

    

    return app
    