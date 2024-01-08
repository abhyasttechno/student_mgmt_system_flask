#import flask framework
from flask import Flask,render_template,request,session,redirect,flash,url_for
import pandas as pd
from passlib.context import CryptContext
from datetime import datetime
import os
from forms import StudentForm,MarksForm,FeesForm,LoginForm,RegisterForm,ForgotForm,ResetForm
# from send_mail_smtp import send_reset_token_email
from models import db,Student,LoginUser,Marks,Fees,pwd_context
from functools import wraps

#initialization flask app
app = Flask(__name__)

app.secret_key = os.urandom(56)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Manu_sid123@localhost/db_school?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

    
def requires_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_status') != 'Admin':
            flash("You do not have permission to access this page.")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function


def requires_teacher(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get('user_status') != 'Teacher':
            flash("You do not have permission to access this page.")
            return redirect(url_for('home'))
        return f(*args, **kwargs)
    return decorated_function



@app.route('/')
def login():
    form = LoginForm()
    return render_template("login.html",form=form)



@app.route('/forgot')
def forgot():
    form = ForgotForm()
    return render_template("forgot.html",form=form)

@app.route('/register')
def register():
    form = RegisterForm()
    return render_template("register.html",form=form)

@app.route('/home')
def home():
    return render_template("home.html")

@app.route('/add_fees')
@requires_admin
def add_fees():
    form = FeesForm()
    return render_template("add_fees.html",form=form)

@app.route('/edit_student')
@requires_admin
def edit_student():
    form = StudentForm()

    students = Student.query.all()
    return render_template("edit_student.html",form=form,payload=students)


@app.route('/student_report')
def student_report():
    students = Student.query.all()
    return render_template("student_report.html",payload=students)

@app.route('/marks_report')
def marks_report():
    marks = Marks.query.all()
    return render_template("marks_report.html",payload=marks)



@app.route('/fee_report')
def fee_report():
    fees = Fees.query.all()
    return render_template("fee_report.html",payload=fees)



@app.route('/edit_marks')
@requires_teacher
def edit_marks():
    form = MarksForm()

    markings = Marks.query.all()
    return render_template("edit_marks.html",form=form,payload=markings)


@app.route('/edit_fees')
@requires_admin
def edit_fees():
    form = FeesForm()

    fees = Fees.query.all()
    return render_template("edit_fees.html",form=form,payload=fees)


@app.route('/edit_stud_fees', methods=['GET', 'POST'])
def edit_stud_fees():
    form = FeesForm()

    if request.method == "POST":
        print("Form is validated")  # Debugging

        reg_num = request.form['regNumber']
        print(f"Registration number from form: {reg_num}")  # Debugging

        # Retrieve the student record based on regNumber
        fee = Fees.query.filter_by(reg_no=reg_num).first()

        if fee:
            print("Fees found")  # Debugging

            # Update the student attributes
            fee.receipt_no = form.receipt_no.data
            fee.class_name = form.class_name.data
            fee.amount = form.amount.data
            fee.dt_deposit = form.dt_deposit.data
            fee.bank = form.bank.data
            fee.fee_reason = form.fee_reason.data
            

            # Commit the changes to the database
            try:
                db.session.commit()
                print("Database updated successfully")  # Debugging
            except Exception as e:
                print(f"Error updating database: {e}")  # Debugging

        else:
            print("Fees not found")  # Debugging

    fee = Fees.query.all()
    return render_template("edit_fees.html", form=form, payload=fee)






@app.route('/edit_stud_marks', methods=['GET', 'POST'])
def edit_stud_marks():
    form = MarksForm()

    if request.method == "POST":
        print("Form is validated")  # Debugging

        reg_num = request.form['regNumber']
        print(f"Registration number from form: {reg_num}")  # Debugging

        # Retrieve the student record based on regNumber
        mark = Marks.query.filter_by(reg_no=reg_num).first()

        if mark:
            print("Student found")  # Debugging

            # Update the student attributes
            mark.exam_name = form.exam_name.data
            mark.language = form.language.data
            mark.english = form.english.data
            mark.maths = form.maths.data
            mark.science = form.science.data
            mark.remarks = form.remarks.data
            

            # Commit the changes to the database
            try:
                db.session.commit()
                print("Database updated successfully")  # Debugging
            except Exception as e:
                print(f"Error updating database: {e}")  # Debugging

        else:
            print("Marks not found")  # Debugging

    marks = Marks.query.all()
    return render_template("edit_student.html", form=form, payload=marks)


@app.route('/edit_stud_details', methods=['GET', 'POST'])
def edit_stud_details():
    form = StudentForm()

    if request.method == "POST":
        print("Form is validated")  # Debugging

        reg_num = request.form['regNumber']
        print(f"Registration number from form: {reg_num}")  # Debugging

        # Retrieve the student record based on regNumber
        student = Student.query.filter_by(reg_no=reg_num).first()

        if student:
            print("Student found")  # Debugging

            # Update the student attributes
            student.student_fullname = form.fullName.data
            student.gender = form.gender.data
            student.dob = form.dob.data
            student.age = form.age.data
            student.phone_no = form.phone.data
            student.email = form.email.data
            student.class_name = form.class_name.data
            student.full_address = request.form['full_address']

            # Commit the changes to the database
            try:
                db.session.commit()
                print("Database updated successfully")  # Debugging
            except Exception as e:
                print(f"Error updating database: {e}")  # Debugging

        else:
            print("Student not found")  # Debugging

    students = Student.query.all()
    return render_template("edit_student.html", form=form, payload=students)

@app.route('/delete_fees', methods=['POST'])
def delete_fees():
    reg_num = request.form['regNumber']
    fee = Fees.query.filter_by(reg_no=reg_num).first()

    if fee:
        db.session.delete(fee)
        db.session.commit()
        flash('Fees deleted successfully!', 'success')
    else:
        flash('Fee not found!', 'danger')
    
    return redirect(url_for('edit_fees'))


@app.route('/delete_mark', methods=['POST'])
def delete_mark():
    reg_num = request.form['regNumber']
    mark = Marks.query.filter_by(reg_no=reg_num).first()

    if mark:
        db.session.delete(mark)
        db.session.commit()
        flash('Mark deleted successfully!', 'success')
    else:
        flash('Mark not found!', 'danger')
    
    return redirect(url_for('edit_marks'))



@app.route('/delete_student', methods=['POST'])
def delete_student():
    reg_num = request.form['regNumber']
    student = Student.query.filter_by(reg_no=reg_num).first()

    if student:
        db.session.delete(student)
        db.session.commit()
        flash('Student deleted successfully!', 'success')
    else:
        flash('Student not found!', 'danger')
    
    return redirect(url_for('edit_student'))


   

@app.route("/logout")
def logout():
    session.clear()
    return redirect('/')


@app.route('/forgot_link', methods=['POST'])
def forgot_link():
    form = ForgotForm()
    if form.validate_on_submit():

        email = form.email.data
   
        user = LoginUser.query.filter_by(email=email).first()
        if user:
            print("email \n",email)
            token = send_reset_token_email(str(email))
            user.token=token
            print("token: ", token)
            db.session.commit()  # Save the updated token to the database
            session.permanent = True
            session['user_id'] = user.email
            flash("Please check your email for Reset Password Link.")
            return render_template("forgot.html",form=form)
        else:
            flash("This email is not registered with us.")
            return render_template("forgot.html",form=form)
        

@app.route('/password_upd', methods=['POST','GET'])
def password_upd():
    print("Starting password_upd function...")
    print("Request method is:", request.method)
    form = ResetForm()
    if form.validate_on_submit():
        print("Form is valid.")
        email = form.email.data
        password = form.password.data
        passw = pwd_context.encrypt(password)
        conf_passw = form.conf_pass.data
        
        dt = datetime.now()
        print("Checking if user exists...")
        user = LoginUser.query.filter_by(email=email).first()
        print("User found: ", user.email)
        print("Form errors:", form.errors)
        if user:
            print("Checking if passwords match...")
            if (password == conf_passw):
                print("matched")
                user.pass_word=passw
                user.dt_time = dt
                db.session.commit()
                session.permanent = True
                session['user_id'] = user.email
                flash("Password reset successful! Proceed to login")
                return render_template("reset.html",form=form)
            else:
                flash("Please enter same password in confirm password.")
                return render_template("reset.html",form=form)
        else:
            flash("Sorry!! This User is not registered with Us. ")
            return render_template("reset.html",form=form)
    else:
        print("Form is Invalid.")
        print(form.errors)
        return render_template("reset.html",form=form)

@app.route('/reset_password/<token>', methods=['GET'])
def reset_password(token):
    token_rec = token
    form = ResetForm()
    user = LoginUser.query.filter_by(token=token_rec).first()
    if not user:
        flash("Invalid Token")
        return render_template("reset.html",form=form)
    form.email.data = user.email
    print("email :\n",user.email)  # Set the email field data
    return render_template("reset.html",form=form)
    
        

@app.route('/login_validation', methods=['POST'])
def login_validation():
    form = LoginForm()
    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data

        user = LoginUser.query.filter_by(email=email).first()

        if user:
            if pwd_context.verify(password, user.pass_word):
                session.permanent = True
                session['user_id'] = user.email
                session['user_status'] = user.user_status

                return render_template("home.html")
            else:
                flash("Kindly provide valid email id and password.")
                return render_template("login.html", form=form)
        else:
            flash("This email id is not registered with us.")
            return render_template("login.html", form=form)


@app.route('/add_user',methods=['POST'])
def add_user():
    form = RegisterForm()
    if form.validate_on_submit():

        email = form.email.data
        password = form.password.data
        passw = pwd_context.encrypt(password)
        conf_passw = form.conf_pass.data
        user_status = form.user_status.data
        dt = datetime.now()
        
        if (password == conf_passw):

            #check the existing user

            user = LoginUser.query.filter_by(email=email).first()

            if user:
            
            
                flash("This email id is already exist")
                return render_template("register.html",form =form)
            
            else:
                token = "default"
                
                user = LoginUser(
                    email=form.email.data,
                    pass_word=passw,
                    token=token,
                    user_status=user_status,
                    dt_time = dt
                )
                db.session.add(user)
                db.session.commit()
                flash("User registered successfully.Kindly Login into the system.")
            return render_template("register.html",form=form)
        else:
            flash("Kindly enter same password in both cases.")
            return render_template("register.html",form=form)
        
    return render_template("register.html",form=form)
    




@app.route('/add_student')
@requires_admin
def add_student():
    form = StudentForm()
    max_reg_no = db.session.query(db.func.coalesce(db.func.max(Student.reg_no), 0)).scalar()
    new_reg_no = max_reg_no + 1
    
    return render_template("student_registration.html", regno=new_reg_no, form=form)



@app.route('/insert_student',methods=['POST'])
def insert_student():
    form = StudentForm()

    if form.validate_on_submit():
        student = Student(
            student_fullname=form.fullName.data,
            gender=form.gender.data,
            dob=form.dob.data,
            age=form.age.data,
            phone_no=form.phone.data,
            email=form.email.data,
            class_name=form.class_name.data,
            full_address=form.address.data
        )

        db.session.add(student)
        db.session.commit()
            
        flash('Student added successfully.', 'success')

    return render_template("student_registration.html",form=form)

@app.route('/insert_fees', methods=['GET', 'POST'])
def insert_fees():
    form = FeesForm()
    if form.validate_on_submit():
        new_fees = Fees(
        reg_no = form.reg_no.data,
        receipt_no = form.receipt_no.data,
        class_name = form.class_name.data,
        amount = form.amount.data,
        dt_deposit = form.dt_deposit.data,
        bank = form.bank.data,
        fee_reason = form.fee_reason.data,
        )

        db.session.add(new_fees)
        db.session.commit()

        flash('Fees added successfully!', 'success')
        return render_template('add_fees.html', form=form)

    return render_template('add_marks.html', form=form)


@app.route('/insert_marks', methods=['GET', 'POST'])
def insert_marks():
    form = MarksForm()
    if form.validate_on_submit():
        reg_no = form.reg_no.data
        exam_name = form.exam_name.data
        language = form.language.data
        english = form.english.data
        maths = form.maths.data
        science = form.science.data
        remarks = form.remarks.data
        email = session.get('email', '')  # retrieve email from session
        dt_time = datetime.now()

        new_mark = Marks(
            reg_no=reg_no,
            exam_name=exam_name,
            language=language,
            english=english,
            maths=maths,
            science=science,
            remarks=remarks,
            email=email,
            dt_time=dt_time
        )

        db.session.add(new_mark)
        db.session.commit()

        flash('Marks added successfully!', 'success')
        return redirect(url_for('insert_marks'))

    return render_template('add_marks.html', form=form)







@app.route('/add_marks')
@requires_teacher
def add_marks():
    form = MarksForm()
    return render_template("add_marks.html", form=form)







if __name__ == '__main__':

    app.run(debug=True, host="localhost", port=8080)
