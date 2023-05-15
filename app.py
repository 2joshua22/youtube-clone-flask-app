from flask import Flask,render_template,redirect,url_for,request
from flask_sqlalchemy import SQLAlchemy
from pytube import extract
import confidential

app=Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"]=confidential.SQLALCHEMY_DATABASE_URI
db=SQLAlchemy(app)
app.app_context().push()

class VideosDB(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String,nullable=False)
    des=db.Column(db.String,nullable=False)
    vurl=db.Column(db.String,nullable=False)
    turl=db.Column(db.String,nullable=False)

    def __repr__(self):
        return "<NAME %r>" %self.name
    
videosdb=VideosDB.query.order_by(VideosDB.id)

@app.route('/')
def home():
    return render_template('index.html',VDB=videosdb)

@app.route('/videoplayer/<V>')
def player(V):
    det=db.session.execute(db.select(VideosDB).filter_by(vurl=V)).scalar_one()
    return render_template('videoplayer.html',Det=det)

@app.route('/upload',methods=["POST","GET"])
def upload():
    if request.method=="POST":
        fvurl=request.form.get("vurl")
        videoid=extract.video_id(fvurl)
        fturl=request.form.get("turl")
        fname=request.form.get("name")
        fdes=request.form.get("des")
        video=VideosDB(name=fname,des=fdes,vurl=videoid,turl=fturl)
        db.session.add(video)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('upload.html',VDB=videosdb)

@app.route('/delete/<I>')
def delete(I):
    video=db.session.execute(db.select(VideosDB).filter_by(id=I)).scalar_one()
    db.session.delete(video)
    db.session.commit()
    return render_template('index.html',VDB=videosdb)

if __name__=="__main__":
    app.run(debug=True)

