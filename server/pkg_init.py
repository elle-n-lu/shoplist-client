import os
from pathlib import Path
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager

BASE_DIR = Path(__file__).resolve().parent

UPLOAD_FOLDER=os.path.join(BASE_DIR,'media')
# print('sfds',UPLOAD_FOLDER)
db=SQLAlchemy()
ma=Marshmallow()
bcrypt=Bcrypt()
jwt=JWTManager()