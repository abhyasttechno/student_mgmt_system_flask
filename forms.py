from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, DateField, SubmitField,PasswordField
from wtforms.validators import DataRequired

class StudentForm(FlaskForm):
    fullName = StringField('Full Name', validators=[DataRequired()])
    gender = SelectField('Gender', choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], validators=[DataRequired()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    
    age = IntegerField('Age', validators=[DataRequired()])
    date_join = DateField('Date of Joining')
    phone = StringField('Phone', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    class_name = StringField('Class', validators=[DataRequired()])
    address = StringField('Full Address', validators=[DataRequired()])
    submit = SubmitField('Submit')


class MarksForm(FlaskForm):
    reg_no = IntegerField('Reg. No.', validators=[DataRequired()])
    exam_name = StringField('Exam Name', validators=[DataRequired()])
    language = IntegerField('Language Marks', validators=[DataRequired()])
    english = IntegerField('English Marks', validators=[DataRequired()])
    maths = IntegerField('Maths Marks', validators=[DataRequired()])
    science = IntegerField('Science Marks', validators=[DataRequired()])
    remarks = StringField('Remarks', validators=[DataRequired()])
    submit = SubmitField('Submit')

class FeesForm(FlaskForm):
    reg_no = IntegerField('Reg. No.', validators=[DataRequired()])
    receipt_no = IntegerField('Receipt No.', validators=[DataRequired()])
    class_name = StringField('Class Name', validators=[DataRequired()])
    amount = IntegerField('Amount of Deposit', validators=[DataRequired()])
    dt_deposit = DateField('Date of Deposit', validators=[DataRequired()])
    bank = StringField('Bank', validators=[DataRequired()])
    fee_reason = StringField('Reason of Payment', validators=[DataRequired()])
    submit = SubmitField('Submit')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class ForgotForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    submit = SubmitField('Reset Password')


class RegisterForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    conf_pass = PasswordField('Confirm Password', validators=[DataRequired()])
    user_status = SelectField('User Type', choices=[('Admin', 'Admin'), ('Teacher', 'Teacher')], validators=[DataRequired()])
    submit = SubmitField('Register')

class ResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    conf_pass = PasswordField('Confirm Password', validators=[DataRequired()])
    
    submit = SubmitField('Reset')
