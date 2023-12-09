import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.svm import LinearSVC
from xgboost import XGBClassifier
from flask import *
import mysql.connector

db = mysql.connector.connect(user="root", password="", port='3306', database='disease')
cur = db.cursor()

app = Flask(__name__)
app.secret_key = "CBJcb786874wrf78chdchsdcv"


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/userhome')
def userhome():
    return render_template('userhome.html')


@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        useremail = request.form['useremail']
        session['useremail'] = useremail
        userpassword = request.form['userpassword']
        sql = "select * from user where Email='%s' and Password='%s'" % (useremail, userpassword)
        cur.execute(sql)
        data = cur.fetchall()
        db.commit()
        if not data:
            msg = "User Credentials Are not valid"
            return render_template("login.html", name=msg)
        else:
            return render_template("userhome.html", myname=data[0][0])
    return render_template('login.html')


@app.route('/registration', methods=["POST", "GET"])
def registration():
    if request.method == 'POST':
        username = request.form['username']
        useremail = request.form['useremail']
        userpassword = request.form['userpassword']
        conpassword = request.form['conpassword']
        Age = request.form['Age']
        contact = request.form['contact']
        if userpassword == conpassword:
            sql = "select * from user where Email='%s' and Password='%s'" % (useremail, userpassword)
            cur.execute(sql)
            data = cur.fetchall()
            db.commit()
            if not data:
                sql = "insert into user(Name,Email,Password,Age,Mob)values(%s,%s,%s,%s,%s)"
                val = (username, useremail, userpassword, Age, contact)
                cur.execute(sql, val)
                db.commit()
                flash("Registered successfully", "success")
                return render_template("login.html")
            else:
                flash("Details are invalid", "warning")
                return render_template("registration.html")
        else:
            flash("Password doesn't match", "warning")
            return render_template("registration.html")
    return render_template('registration.html')


@app.route('/diabetes', methods=['POST', 'GET'])
def diabetes():
    if request.method == "POST":
        Pregnancies = float(request.form['Pregnancies'])
        Glucose = float(request.form['Glucose'])
        BloodPressure = float(request.form['BloodPressure'])
        SkinThickness = float(request.form['SkinThickness'])
        Insulin = float(request.form['Insulin'])
        BMI = float(request.form['BMI'])
        DiabetesPedigreeFunction = float(request.form['DiabetesPedigreeFunction'])
        Age = float(request.form['Age'])

        lee = [Pregnancies, Glucose, BloodPressure, SkinThickness, Insulin, BMI, DiabetesPedigreeFunction, Age]

        import pickle
        filename = 'DecisionTreeClassifier(diabetes).sav'
        model = pickle.load(open(filename, 'rb'))
        result = model.predict([lee])
        result = result[0]
        if result == 0:
            msg = "The Person has NO-Diabetes"
        elif result == 1:
            msg = "The Person has Diabetes"
        return render_template("diabetes.html", msg=msg)
    return render_template("diabetes.html")


if __name__ == '__main__':
    app.run(debug=True)
