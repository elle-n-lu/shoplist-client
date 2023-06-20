from pkg_init import db, ma
from marshmallow import fields

class Plan(db.Model):
    __tablename__='plans'
    id=db.Column(db.Integer, primary_key=True)
    # product_price = db.Column(db.String())
    list_of_items = db.Column(db.JSON)
    # product_name = db.Column(db.String())
    date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())
    uploadfile_id = db.Column(db.Integer, db.ForeignKey("uploadfiles.id"), nullable=False)
    cost = db.relationship(
        "Cost",
        backref="plan",
        uselist=False,
        cascade="all, delete"
    )

class PlanSchema(ma.Schema):
    class Meta:
        fields=("id","list_of_items","cost")
    # cost = fields.List(fields.Nested("CostSchema"))
    cost = fields.Nested("CostSchema")
