from pkg_init import db, ma
from marshmallow import fields

class Uploadfile(db.Model):
    __tablename__='uploadfiles'
    id=db.Column(db.Integer, primary_key=True)
    budget = db.Column(db.Float)
    file_name = db.Column(db.String())
    file=db.Column(db.LargeBinary)
    date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())
    # FK of users entity
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    # relation to plans entity
    plans = db.relationship(
        "Plan",
        backref="uploadfile",
        cascade="all, delete"
    )
    comments = db.relationship(
        "Comment",
        backref="uploadfile",
        cascade="all, delete"
    )

class UploadfileSchema(ma.Schema):
    class Meta:
        fields=("id","budget","file_name","plans","comments","date","user_id")
    plans = fields.List(fields.Nested("PlanSchema"))
    comments=fields.List(fields.Nested("CommentSchema"))
