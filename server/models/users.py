from pkg_init import db, ma

from marshmallow import fields

class User(db.Model):
    __tablename__='users'
    id=db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(),nullable=False)
    email = db.Column(db.String(),nullable=False, unique=True)
    password = db.Column(db.String(),nullable=False,)
    admin = db.Column(db.Boolean(), default=False)
    date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())
    uploadfiles = db.relationship(
        "Uploadfile",
        backref="user",
        cascade="all, delete"
    )
    comments = db.relationship(
        "Comment",
        backref="user",
        cascade="all, delete"
    )

class UserSchema(ma.Schema):
    class Meta:
        fields=("id","username","email","admin","password","uploadfiles")
    # also can exclue password here or later in auth-controller
    uploadfiles = fields.List(fields.Nested("UploadfileSchema", exclude=("plans",)))

