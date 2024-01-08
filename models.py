# password context for encrypting password using cryptography
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.context import CryptContext

db = SQLAlchemy()

pwd_context = CryptContext(
    schemes=["pbkdf2_sha256"],
    default="pbkdf2_sha256",
    pbkdf2_sha256__default_rounds=30000
)

class Student(db.Model):
    __tablename__ = 'tbl_student_details'
    reg_no = db.Column(db.Integer, primary_key=True)
    student_fullname = db.Column(db.String(100))
    gender = db.Column(db.String(50))
    dob = db.Column(db.Date)
    age = db.Column(db.Integer)
    phone_no = db.Column(db.String(20))
    email = db.Column(db.String(100))
    class_name = db.Column(db.String(50))
    full_address = db.Column(db.Text)
    date_join = db.Column(db.DateTime, default=datetime.utcnow)


class LoginUser(db.Model):
    __tablename__ = 'tbl_login_user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), unique=True, nullable=True)
    pass_word = db.Column(db.String(100), nullable=True)
    token = db.Column(db.String(500), nullable=True)
    user_status = db.Column(db.String(50), nullable=True)
    dt_time = db.Column(db.DateTime, nullable=True)

class Marks(db.Model):
    __tablename__ = 'tbl_marks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reg_no = db.Column(db.Integer, nullable=False)
    exam_name = db.Column(db.String(200), nullable=True)
    language = db.Column(db.Integer, nullable=False)
    english = db.Column(db.Integer, nullable=False)
    maths = db.Column(db.Integer, nullable=False)
    science = db.Column(db.Integer, nullable=False)
    remarks = db.Column(db.String(200), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    dt_time = db.Column(db.DateTime, nullable=True)

class Fees(db.Model):
    __tablename__ = 'tbl_fees'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    reg_no = db.Column(db.Integer, nullable=False)
    receipt_no = db.Column(db.Integer, nullable=False)
    class_name = db.Column(db.String(200), nullable=True)
    amount = db.Column(db.Integer, nullable=False)
   
    dt_deposit = db.Column(db.DateTime, nullable=True)
    bank = db.Column(db.String(200), nullable=True)
    fee_reason = db.Column(db.String(500), nullable=True)