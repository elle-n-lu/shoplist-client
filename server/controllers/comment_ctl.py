from flask import Blueprint, jsonify, request
from flask_jwt_extended import get_jwt_identity, jwt_required
from models.users import User
from models.uploadfiles import Uploadfile
from pkg_init import db
from models.comments import Comment, CommentSchema

app_comments=Blueprint("comment", __name__,url_prefix='/files/<int:id>/comment')

@app_comments.route("/",methods=['GET'])
@jwt_required()
def get_comments(id):
    user_id=get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    uploadfile=Uploadfile.query.filter_by(id=id).first()
    if user:
        if uploadfile:
            comments=Comment.query.all()
    
            result=CommentSchema(many=True).dump(comments)
            return jsonify(result)
        else:
            return "uploadfile not exist"
    else:
        return {"error":"invalid user"}


@app_comments.route("/create",methods=['POST'])
@jwt_required()
def create_comment(id):
    user_id=get_jwt_identity()
    user = User.query.filter_by(id=user_id).first()
    uploadfile=Uploadfile.query.filter_by(id=id).first()
    if user:
        if uploadfile:
            comment_info=CommentSchema().load(request.json)
            new_comment=Comment(
                message=comment_info['message'],
                user_id=user.id,
                uploadfile_id=id
            )
            db.session.add(new_comment)
            db.session.commit()
    
            result=CommentSchema().dump(new_comment)
            return jsonify(result)
        else:
            return "uploadfile not exist"
    else:
        return {"error":"invalid user"}