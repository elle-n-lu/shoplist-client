

from flask import Blueprint, jsonify
from models.costs import Cost,CostSchema

app_costs=Blueprint("cost", __name__,url_prefix='/costs')

@app_costs.route("/",methods=['GET'])
# @jwt_required()
def get_costs():
    # user_id=get_jwt_identity()
    # user = User.query.filter_by(id=user_id).first()
    # if user:
    costs=Cost.query.all()
    # print(costs)
    result=CostSchema(many=True).dump(costs)
    return jsonify(result)