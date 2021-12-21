from enum import unique
from wtforms.fields.core import StringField
from app import db, login
from sqlalchemy.schema import Sequence
from datetime import date
from flask_login import UserMixin
 
class taikhoan(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    tendangnhap = db.Column(db.String(50), unique=True)
    matkhau = db.Column(db.String(50))
    def __init__(self, tendangnhap, matkhau):
        self.tendangnhap = tendangnhap
        self.matkhau = matkhau
    def __repr__(self):
        return '<taikhoan {} {}>'.format(self.tendangnhap,self.matkhau)

class loaisach(db.Model):
    maloai = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tenloai = db.Column(db.String(255))

    def __repr__(self):
        return f"<loaisach> {self.maloai}:{self.tenloai}"

class sach(db.Model):
    masach = db.Column(db.Integer, primary_key=True, autoincrement=True)
    tensach = db.Column(db.String(255))
    maloai = db.Column(db.Integer, db.ForeignKey('loaisach.maloai'))
    tenloaisach = db.Column(db.String(255))
    tacgia = db.Column(db.String(255))
    nhaxuatban = db.Column(db.String(255))
    soluong = db.Column(db.Integer)
    gia = db.Column(db.Integer)

    def __repr__(self):
        return f"<sach> {self.masach}:{self.tensach}"

class sinhvien(db.Model):
    masv = db.Column(db.String(50), primary_key=True)
    hoten = db.Column(db.String(255))
    diachi = db.Column(db.String(255))
    nganh = db.Column(db.String(255))
    khoa = db.Column(db.String(255))
    sodt = db.Column(db.String(255))

    def __repr__(self):
        return f"<sinhvien> {self.masv}:{self.hoten}"

class donmuon(db.Model):
    madonmuon = db.Column(db.Integer, primary_key=True, autoincrement=True)
    masv = db.Column(db.String(50), db.ForeignKey('sinhvien.masv'))
    hoten = db.Column(db.String(255))
    masach = db.Column(db.Integer, db.ForeignKey('sach.masach'))
    tensach = db.Column(db.String(255))
    ngaymuon =  db.Column(db.Date, index=True)                              
    hantra = db.Column(db.Date, index=True)
    trangthai = db.Column(db.String(255))

    def __repr__(self):
        return f"<sinhvien> {self.madonmuon}:{self.hoten}:{self.tensach}:{self.ngaymuon}:{self.hantra}:{self.trangthai}"

@login.user_loader
def load_user(id):
    return taikhoan.query.get(int(id))