
from flask import Flask
from flask_cors import CORS
from pkg_init import db, ma, bcrypt, jwt
from cli_commands.cli_command_ctl import db_commands
from controllers.auth_ctl import app_auth
from controllers.uploadfile_ctl import app_file_upload
from controllers.plan_ctl import app_plans
from controllers.cost_ctl import app_costs
from controllers.comment_ctl import app_comments
controllers = [app_auth, app_file_upload, app_plans, app_costs, app_comments]

def set_up():
    app= Flask(__name__)
    app.config.from_object("config.app_config")
    CORS(app,origins=[
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "https://shop-plan.netlify.app",
],supports_credentials=True)
    # app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

    db.init_app(app)
    ma.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    @app.errorhandler(401)
    def unauthorised(err):
        return {"error":"You must be an admin"}, 401

    app.register_blueprint(db_commands)
    for controller in controllers:
        app.register_blueprint(controller)


    return app
