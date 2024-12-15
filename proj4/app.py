from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import func
from flask import render_template
from flask import request


app = Flask(__name__)
#mysql://username:password@host:port/database_name
app.config['SECRET_KEY']='test-key'
#pay attention to this line,.
app.config['SQLALCHEMY_DATABASE_URI']= 'mysql+pymysql://root:quimica@mysqldb:3306/my_person_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
db = SQLAlchemy(app)


class Persons(db.Model):
    """ person_id int AUTO_INCREMENT primary key,
    fname varchar(100),
    lname varchar(100),
    email varchar(100)); """

    person_id = db.Column(db.Integer,primary_key=True)
    fname = db.Column(db.String(100))
    lname = db.Column(db.String(100))
    email = db.Column(db.String(100))

@app.route("/add",methods=['GET','POST'])
def add_userdata():
    return render_template('add_person.html')

@app.route("/process_userdata", methods=['GET',"POST"])
def process_userdata():
    fname = request.form['fname']
    lname = request.form['lname']
    email = request.form['email']

    #now save this info to the db
    person = Persons(fname=fname,lname=lname,email=email)
    db.session.add(person)
    db.session.commit()

    last_item = Persons.query.order_by(Persons.person_id.desc()).first()

    #pending...
    #save info in the DB
    #retrieve info from the DB and populate fname,lname,email (select the last entry, that is the info we use to populate)

    return render_template("view_persons.html",fname=last_item.fname,lname=last_item.lname,email=last_item.email)

@app.route("/view_all", methods=['GET'])
def view_all():
    all_records = Persons.query.all()
    return render_template("view_persons.html",all_records=all_records)


@app.route("/doit",methods=['GET'])
def doit():
    fname="aida-rosa"
    lname="Ocana"
    email="ocaquin@gmail.com"

    person = Persons(fname=fname,lname=lname,email=email)
    db.session.add(person)
    db.session.commit()
    return "ok"

if __name__ == "__main__":
    app.run(debug="True",host="0.0.0.0")