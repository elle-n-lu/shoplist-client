import os
from flask import Blueprint, jsonify,request
from pkg_init import db, bcrypt, UPLOAD_FOLDER
from flask_jwt_extended import get_jwt_identity,jwt_required
from werkzeug.utils import secure_filename
from models.uploadfiles import Uploadfile, UploadfileSchema
from models.costs import Cost, CostSchema
from models.plans import Plan, PlanSchema
from models.users import User,UserSchema
from terminal_app.main import get_plans

app_file_upload=Blueprint("uploadfile", __name__,url_prefix='/files')

ALLOWED_EXTENSIONS = {'txt', }
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app_file_upload.route("/",methods=['GET'])
@jwt_required()
def get_files():
    user_id=get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user:
        files=Uploadfile.query.all()
        res=UploadfileSchema(many=True).dump(files)
        return jsonify(res)
    else:
        return {"error":"login required"}, 401
    
@app_file_upload.route("/<int:id>",methods=['GET'])
@jwt_required()
def get_file(id):
    user_id=get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user:
        file=Uploadfile.query.filter_by(id=id).first()
        res=UploadfileSchema().dump(file)
        return jsonify(res)
    else:
        return {"error":"login required"}, 40

@app_file_upload.route("/upload",methods=['POST'])
@jwt_required()
def upload_files():
    user_id=get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user:
        try:
            file = request.files['uploadfile']
            budget = request.form['budget']
            file_name = secure_filename(file.filename)
            if file and allowed_file(file.filename):
                file.save(os.path.join(UPLOAD_FOLDER, file_name))
                newfile=Uploadfile(
                    budget=budget,
                    file_name=file_name,
                    file=file.read(),
                    user_id=1
                )
                db.session.add(newfile)
                db.session.commit()
                uploadfile_id = UploadfileSchema().dump(newfile)['id']
                
                plans_res=get_plans(float(budget),os.path.join(UPLOAD_FOLDER, file_name))
                if plans_res:
                    for plan in plans_res:
                        for key, val in plan.items():
                            list_items=[]
                            for i in val:
                                list_items.append({"title":i[0],"price":i[1]})
                            new_plan = Plan(list_of_items=list_items, uploadfile_id=uploadfile_id)
                            db.session.add(new_plan)
                            db.session.commit()

                            plan_id = PlanSchema().dump(new_plan)['id']

                            new_cost=Cost(total_cost=str(key), plan_id=plan_id)
                            db.session.add(new_cost)
                            db.session.commit()


                    # print('sds',plans_res)
                    # print('file uploaded '+ file.filename+" to the database "+ os.path.join(UPLOAD_FOLDER, file_name))
                    result = UploadfileSchema().dump(newfile)
                    return jsonify(result)
                else:
                    return {"error":"no plans found"}
            else:
                return {'error':"only txt file accepted"},401
        except KeyError:
            return {"error":"bad request"},415
    else:
        return {"error":"login required"}, 401
    
@app_file_upload.route("/delete/<int:id>/",methods=['DELETE'])
@jwt_required()
def delete_files(id):
    user_id=get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    if user:
        try:
            file = Uploadfile.query.filter_by(id=id).first()
            if not file:
                return {"error":"file not found"}, 400
            db.session.delete(file)
            db.session.commit()
            return "file deleted"
        except KeyError:
            return {"error":"bad request"},415
    else:
        return {"error":"login required"}, 401