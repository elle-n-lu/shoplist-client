from pkg_init import db, ma


class Cost(db.Model):
    __tablename__='costs'
    id=db.Column(db.Integer, primary_key=True)
    total_cost = db.Column(db.String())
    date = db.Column(db.DateTime(timezone=True), server_default=db.sql.func.now())
    plan_id = db.Column(db.Integer, db.ForeignKey("plans.id"), nullable=False)

class CostSchema(ma.Schema):
    class Meta:
        fields=("id","total_cost")