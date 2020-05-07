from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
import sqlite3,os,itertools
from werkzeug.utils import secure_filename

app=Flask(__name__)
UPLOAD_FOLDER="./uploads"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///test.db"
db=SQLAlchemy(app)
d={}
curremail=None
fields=['First Name','Last Name','Email ID','Phone Number']
class Account(db.Model):
    firstname=db.Column(db.String(50),nullable=False)
    lastname=db.Column(db.String(50),nullable=False)
    email=db.Column(db.String(100),primary_key=True)
    password=db.Column(db.String(16),nullable=False)
    phno=db.Column(db.String(12))
    image=db.Column(db.String(100))

    def __repr__(self):
        return self.id

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/index.html")
def idx():
    return render_template("index.html")

@app.route("/mainpage.html",methods=['POST','GET'])
def mainpage():
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        password=request.form['pw']
        phoneno=request.form['phoneno']
        email=request.form['email']
        myfile=request.files['image']
        filename=secure_filename(myfile.filename)
        myfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        new_acc=Account(firstname=firstname,lastname=lastname,email=email,password=password,phno=phoneno,image=filename)
        db.session.add(new_acc)
        db.session.commit()
        return redirect('/accountmade.html')
    else:
        return render_template("mainpage.html")

@app.route("/accountmade.html")
def accountmade():
    return render_template("accountmade.html")

@app.route("/login.html",methods=['POST','GET'])
def login():
    if request.method=='POST':
        email=request.form['email']
        password=request.form['pw']
        curr=Account.query.filter_by(email=email).first()
        if curr is None:
            return render_template("tryagain.html")
        if(curr.password==password):
            global curremail
            curremail=email
            return redirect('/welcome.html')
        else:
            return render_template("tryagain.html")
    else:
        return render_template("login.html")

@app.route('/welcome.html',methods=['POST','GET'])
def welcome():
    global curremail
    if request.method=='GET':
        curr=Account.query.filter_by(email=curremail).first()
        data=[curr.firstname,curr.lastname,curr.email,curr.phno]
        global fields
        for i in range(4):
            d[fields[i]]=data[i]
        return render_template('welcome.html',keys=d.keys(),d=d)
    
    if request.method=='POST':
        firstname=request.form['firstname']
        lastname=request.form['lastname']
        password=request.form['pw']
        phoneno=request.form['phoneno']
        email=request.form['email']
        myfile=request.files['image']
        
        curr=Account.query.filter_by(email=curremail).first()
        if firstname!="":
            curr.firstname=firstname
        if lastname!="":
            curr.lastname=lastname
        if password!="":
            curr.password=password
        if phoneno!="":
            curr.phno=phoneno
        if email!="":
            curr.email=email
        if myfile.filename!="":
            filename=secure_filename(myfile.filename)
            myfile.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            curr.image=filename
        db.session.commit()
        curremail=curr.email
        return redirect('/changes.html')

@app.route('/changes.html')
def changes():
    curr=Account.query.filter_by(email=curremail).first()
    data=[curr.firstname,curr.lastname,curr.email,curr.phno]
    global fields
    for i in range(4):
        d[fields[i]]=data[i]
    return render_template('changes.html',keys=d.keys(),d=d)

if(__name__=="__main__"):
    app.run(debug=True)
