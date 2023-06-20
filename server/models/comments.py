from pkg_init import db,ma

class Comment(db.Model):
    # define the table name for the db
    __tablename__= "comments"

    id = db.Column(db.Integer,primary_key=True)
    # Add the rest of the attributes. 
    message= db.Column(db.String())
    # two foreign keys
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    uploadfile_id = db.Column(db.Integer, db.ForeignKey("uploadfiles.id"), nullable=False)

class CommentSchema(ma.Schema):
    class Meta:
        fields=("id","message")
    