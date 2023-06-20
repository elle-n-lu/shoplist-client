

from flask import Blueprint, jsonify
from models.plans import Plan,PlanSchema

app_plans=Blueprint("plan", __name__,url_prefix='/plans')

@app_plans.route("/",methods=['GET'])
# @jwt_required()
def get_plans():
    # user_id=get_jwt_identity()
    # user = User.query.filter_by(id=user_id).first()
    # if user:
    plans=Plan.query.all()
    print(plans)
    result=PlanSchema(many=True).dump(plans)
    return jsonify(result)
   
    # else:
    #     return {"error":"login required"}, 401