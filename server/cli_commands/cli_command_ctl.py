from flask import Blueprint
from pkg_init import db, bcrypt
from models.users import User
from models.uploadfiles import Uploadfile
from models.plans import Plan
from models.costs import Cost
from models.comments import Comment

db_commands=Blueprint("db",__name__)

@db_commands.cli.command("create")
def create_db():
    db.create_all()
    print("tables created")

@db_commands.cli.command("seed")
def seed_db():
    admin=User(
        username = "admin",
        email ="admin@email.com",
        password = bcrypt.generate_password_hash("admin").decode("utf-8"),
        admin = True,
    )
    db.session.add(admin)
    db.session.commit()

    print("tables seeded")

@db_commands.cli.command("drop")
def drop_db():
    db.drop_all()
    print('tables dropped')

