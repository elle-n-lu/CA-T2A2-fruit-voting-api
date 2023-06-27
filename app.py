from flask import Flask
from pkg_init import db,ma, bcrypt, jwt
from cli_commands.command_ctl import db_commands
from controllers.admin_ctl import app_admin
from controllers.user_ctl import app_user
from controllers.fruit_ctl import app_fruit
from controllers.specie_ctl import app_specie
from controllers.comment_ctl import app_comment
from controllers.vote_ctl import app_vote

controllers=[app_admin, app_user, app_fruit, app_specie, app_vote, app_comment]

def setup():
    app=Flask(__name__)
    app.config.from_object("config.app_config")

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(401)
    def unauthorised(err):
        return {"error":"You are not authorised"}, 401
    
    @app.route("/",methods=['GET'])
    def say_hello():
        return 'hi there'
    
    app.register_blueprint(db_commands)
    for controller in controllers:
        app.register_blueprint(controller)

    return app
    