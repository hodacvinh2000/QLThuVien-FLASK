from typing import ValuesView
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.core import DateField, IntegerField
from wtforms.fields.simple import TextAreaField
from wtforms.validators import DataRequired
from wtforms.widgets.core import TextArea
from app.models import sinhvien

class LoginForm(FlaskForm):
    username = StringField("Tên đăng nhập", validators=[DataRequired()])
    password = PasswordField("Mật khẩu", validators=[DataRequired()])
    submit = SubmitField("Đăng nhập")

class AddSvForm(FlaskForm):
    masv = StringField("Mã sinh viên", validators=[DataRequired()])
    hoten = StringField("Họ và tên", validators=[DataRequired()])
    diachi = StringField("Địa chỉ", validators=[DataRequired()])
    nganh = StringField("Ngành học", validators=[DataRequired()])
    khoa = StringField("Khóa", validators=[DataRequired()])
    sodt = StringField("Số điện thoại", validators=[DataRequired()])
    submit = SubmitField("Đồng ý")

class TimSvForm(FlaskForm):
    key = StringField("")
    submit = SubmitField("Tìm")

class addDonMuonForm(FlaskForm):
    madonmuon = StringField("Mã đơn mượn", validators=[DataRequired()])
    masv = StringField("Mã sinh viên", validators=[DataRequired()])
    hoten = StringField("Họ tên", validators=[DataRequired()])
    masach = IntegerField("Mã sách", validators=[DataRequired()])
    tensach = StringField("Khóa", validators=[DataRequired()])
    ngaymuon = DateField("Ngày mượn", validators=[DataRequired()])
    hantra = DateField("Hạn trả", validators=[DataRequired()])
    trangthai = StringField("Trạng thái", validators=[DataRequired()])
    submit = SubmitField("Đồng ý")