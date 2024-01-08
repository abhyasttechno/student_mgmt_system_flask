from flask import Flask,render_template,request,session,flash
import pandas as pd
import pymysql.cursors
from passlib.context import CryptContext
from datetime import datetime
import os

# password context for encrypting password using cryptography
pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)

# setting up mysql connection
connection = pymysql.connect(host='localhost',
                             user='root',
                             password='p@ssw0rd',
                             db='db_sms',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)


app.secret_key = os.urandom(56)


@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        email=request.form['email']
        password = request.form['pass']
        passw = pwd_context.encrypt(password)
        dt = datetime.now()

        with connection.cursor() as cursor:
                
            sql = "SELECT email,pass_word,token FROM `tbl_login_user` WHERE `email` = %s"
            cursor.execute(sql, email)
            items = cursor.fetchall()
        
        # If account exists show error and validation checks
        if items:
            flash("This email id is already exist")
            return render_template("login.html")
        else:
            with connection.cursor() as cursor:
                token = "default"
                sql = "INSERT INTO `tbl_login_user`(`email`, `pass_word`, `token`,`dt_time`) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (email, passw, token, "registered", "user", dt))
                connection.commit()
                cursor.close()
                flash("User registered successfully.")
            return render_template('login.html')

    return render_template("login.html")


@app.route('/login_validation', methods=['POST'])
def login_validation():
    if request.method == 'POST':

        email=request.form['email']
        password = request.form['pass']
        print("password",password)

        with connection.cursor() as cursor:
            statement = "select email,pass_word from `tbl_login_user` where `email`=%s"
            cursor.execute(statement, email)
            items = cursor.fetchall()

        for item in items:
            hashed=item['pass_word']

        if items and (pwd_context.verify(password, hashed)) == True:
            
            print("password",hashed)
            
            session.permanent = True
            session['user_id'] = email

            return render_template("home.html")
        else:
            flash("Kindly provide valid email id & password")
            return render_template("login.html")
        

@app.route('/add_user',methods=['POST'])
def add_user():
    if request.method=="POST":

        email = request.form['email']
        password = request.form["pass"]
        passw = pwd_context.encrypt(password)
        dt = datetime.now()

        #check the existing user

        with connection.cursor() as cursor:
                
            statement = "SELECT email,pass_word,token FROM `tbl_login_user` WHERE `email` = %s"
            cursor.execute(statement, email)
            items = cursor.fetchall()
        
        # If account exists show error and validation checks
        if items:
            flash("This email id is already exist")
            return render_template("register.html")
        else:
            with connection.cursor() as cursor:
                token = "default"
                statement = "INSERT INTO `tbl_login_user`(`email`, `pass_word`, `token`,`dt_time`) VALUES (%s, %s, %s, %s)"
                cursor.execute(statement, (email, passw, token, dt))
                connection.commit()
                cursor.close()
                flash("User registered successfully.Kindly Login into the system.")
        return render_template('register.html')