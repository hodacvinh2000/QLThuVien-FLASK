from flask import render_template, request, redirect, session
from flask.helpers import flash
from flask_login.utils import login_required
from app import app, db
from app.forms import LoginForm, AddSvForm, TimSvForm
from app.models import sinhvien, taikhoan, loaisach, sach, donmuon
from flask_login import current_user, logout_user, login_user
from werkzeug.urls import url_parse
from datetime import date
import hashlib

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# Đăng nhập
@app.route('/login', methods=["get","post"])
def login():
    if request.method == "POST":
        tendangnhap = request.form.get("tendangnhap")
        matkhau = request.form.get("matkhau")
        matkhau = str(hashlib.md5(matkhau.strip().encode("utf-8")).hexdigest())

        user = taikhoan.query.filter(taikhoan.tendangnhap==tendangnhap,taikhoan.matkhau==matkhau).first()
        if user:
            login_user(user=user)
            return redirect('/index')
        else:
            return render_template('index.html', dangnhapsai=1)

# Đăng xuất
@app.route('/logout')
def logout():
    logout_user()
    return redirect('/index')

# Sinh viên
@app.route('/sinhvien', methods=["get","post"])
def ds_sinhvien():
    if current_user.is_authenticated:
        key = request.form.get("key")
        dssv = sinhvien.query.all()
        if key != None:
            if key != "":
                dssv = sinhvien.query.filter(sinhvien.masv.like('%'+key+'%')
                                        |sinhvien.hoten.like('%'+key+'%')
                                        |sinhvien.diachi.like('%'+key+'%')
                                        |sinhvien.nganh.like('%'+key+'%')
                                        |sinhvien.sodt.like('%'+key+'%')).all()
            else:
                dssv = []
        themsv = None
        xoasv = None
        capnhatsv = None    
        if 'themsv' in session:
            themsv = 1
            session.pop('themsv',None)
        if 'xoasv' in session:
            xoasv = 1
            session.pop('xoasv',None)
        if 'capnhatsv' in session:
            capnhatsv = 1
            session.pop('capnhatsv',None)
        return render_template('sinhvien.html',dssv=dssv,themsv=themsv,xoasv=xoasv,capnhatsv=capnhatsv)
    return render_template('index.html')

@app.route('/themsinhvien', methods=["get","post"])
def themsinhvien():
    if current_user.is_authenticated:
        if request.method == "POST":
            masv = request.form.get("masv")
            hoten = request.form.get("hoten")
            diachi = request.form.get("diachi")
            nganh = request.form.get("nganh")
            khoa = request.form.get("khoa")
            sodt = request.form.get("sodt")
            # Kiểm tra trùng mã sinh viên
            dssv = sinhvien.query.where(sinhvien.masv==masv).all()
            if len(dssv) > 0:
                return render_template('formsinhvien.html',trungmasv=1,sv=None) 
            else:
                sv = sinhvien(masv=masv,hoten=hoten,diachi=diachi,nganh=nganh,khoa=khoa,sodt=sodt)
                db.session.add(sv)  
                db.session.commit()
                session['themsv'] = 1
                return redirect('/sinhvien')
        return render_template('formsinhvien.html', sv=None)
    return render_template('index.html')
@app.route('/capnhatsinhvien/<masvcu>', methods=["get","post"])
def capnhatsinhvien(masvcu):
    if current_user.is_authenticated:
        if request.method == "POST":
            masv = request.form.get("masv")
            hoten = request.form.get("hoten")
            diachi = request.form.get("diachi")
            nganh = request.form.get("nganh")
            khoa = request.form.get("khoa")
            sodt = request.form.get("sodt")
            sinhviencu = sinhvien(masv=masvcu,hoten=hoten,diachi=diachi,nganh=nganh,khoa=khoa,sodt=sodt)
            if (masv!=masvcu):
                # Kiểm tra trùng mã sinh viên 
                dssv = sinhvien.query.where(sinhvien.masv==masv).all()
                if len(dssv) > 0:
                    return render_template('formsinhvien.html',trungmasv=1,sv=sinhviencu) 
            sv = sinhvien.query.filter(sinhvien.masv==masvcu).first()
            sv.masv = masv
            sv.hoten = hoten
            sv.diachi = diachi
            sv.nganh = nganh
            sv.khoa = khoa
            sv.sodt = sodt
            db.session.commit()
            session['capnhatsv'] = 1
            return redirect('/sinhvien')

        sv = sinhvien.query.filter(sinhvien.masv==masvcu).first()
        return render_template('formsinhvien.html',sv=sv)
    return render_template('index.html')
@app.route('/xoasinhvien/<masv>', methods=["get","post"])
def xoasinhvien(masv):
    if current_user.is_authenticated:
        sv = sinhvien.query.filter(sinhvien.masv==masv).first()
        db.session.delete(sv)
        db.session.commit()
        session['xoasv'] = 1
        return redirect('/sinhvien')
    return render_template('index.html')

# Loại sách
@app.route('/loaisach', methods=["get","post"])
def ds_loaisach():
    if current_user.is_authenticated:
        key = request.form.get("key")
        dsloaisach = loaisach.query.all()
        if key != None:
            if key != "":
                dsloaisach = loaisach.query.filter(loaisach.tenloai.like('%'+key+'%')).all()
            else:
                dsloaisach = []
        themloai = None
        xoaloai = None
        capnhatloai = None    
        if 'themloai' in session:
            themloai = 1
            session.pop('themloai',None)
        if 'xoaloai' in session:
            xoaloai = 1
            session.pop('xoaloai',None)
        if 'capnhatloai' in session:
            capnhatloai = 1
            session.pop('capnhatloai',None)
        return render_template('loaisach.html',dsloaisach=dsloaisach,themloai=themloai,xoaloai=xoaloai,capnhatloai=capnhatloai)
    return render_template('index.html')

@app.route('/themloaisach', methods=["get","post"])
def themloaisach():
    if current_user.is_authenticated:
        if request.method == "POST":
            tenloai = request.form.get("tenloai")
            dsloai = loaisach.query.where(loaisach.tenloai==tenloai).all()
            if len(dsloai) > 0: 
                return render_template('formloaisach.html',trungtenloai=1,loaisach=None) 
            else:
                ls = loaisach(tenloai=tenloai)
                db.session.add(ls)  
                db.session.commit()
                session['themloai'] = 1
                return redirect('/loaisach')
        return render_template('formloaisach.html', loaisach=None)
    return render_template('index.html')
@app.route('/capnhatloaisach/<maloai>', methods=["get","post"])
def capnhatloaisach(maloai):
    if current_user.is_authenticated:
        if request.method == "POST":
            tenloaisach = request.form.get("tenloai")
            tenloaicu = request.form.get("tenloaicu")
            loaisachcu = loaisach(maloai=maloai,tenloai=tenloaicu)
            if (tenloaisach!=tenloaicu):
                # Kiểm tra trùng tên loại sách
                dsloaisach = loaisach.query.where(loaisach.tenloai==tenloaisach).all()
                if len(dsloaisach) > 0:
                    return render_template('formsinhvien.html',trungtenloai=1,loaisach=loaisachcu) 
            loai = loaisach.query.filter(loaisach.maloai==maloai).first()
            loai.tenloai = tenloaisach
            db.session.commit()
            session['capnhatloai'] = 1
            return redirect('/loaisach')

        ls = loaisach.query.filter(loaisach.maloai==maloai).first()
        return render_template('formloaisach.html',loaisach=ls)
    return render_template('index.html')
@app.route('/xoaloaisach/<maloai>', methods=["get","post"])
def xoaloaisach(maloai):
    if current_user.is_authenticated:
        ls = loaisach.query.filter(loaisach.maloai==maloai).first()
        dssach = sach.query.filter(sach.maloai==maloai).all()
        for s in dssach:
            dsdonmuon = donmuon.query.filter(donmuon.masach==s.masach).all()
            for don in dsdonmuon:
                db.session.delete(don)
            db.session.delete(s)
        db.session.delete(ls)
        db.session.commit()
        session['xoaloai'] = 1
        return redirect('/loaisach')
    return render_template('index.html')

# Sách
@app.route('/sach', methods=["get","post"])
def ds_sach():
    if current_user.is_authenticated:
        key = request.form.get("key")
        dssach = sach.query.all()
        if key != None:
            if key != "":
                dssach = sach.query.filter(sach.tenloaisach.like('%'+key+'%')|sach.tacgia.like('%'+key+'%')|sach.nhaxuatban.like('%'+key+'%')).all()
            else:
                dssach = []
        themsach = None
        xoasach = None
        capnhatsach = None    
        if 'themsach' in session:
            themsach = 1
            session.pop('themsach',None)
        if 'xoasach' in session:
            xoasach = 1
            session.pop('xoasach',None)
        if 'capnhatsach' in session:
            capnhatsach = 1
            session.pop('capnhatsach',None)
        return render_template('sach.html',dssach=dssach,themsach=themsach,xoasach=xoasach,capnhatsach=capnhatsach)
    return render_template('index.html')

@app.route('/themsach', methods=["get","post"])
def themsach():
    if current_user.is_authenticated:
        dsloaisach  = loaisach.query.all()
        if request.method == "POST":
            tensach = request.form.get("tensach")
            tacgia = request.form.get("tacgia")
            nhaxuatban = request.form.get("nhaxuatban")
            soluong = request.form.get("soluong")
            gia = request.form.get("gia")
            maloai = request.form.get("maloai")
            dssach = sach.query.where(sach.tensach==tensach).all()
            ls = loaisach.query.filter(loaisach.maloai==maloai).first() 
            tl = ls.tenloai  
            if len(dssach) > 0: 
                return render_template('formsach.html',trungten=1,sach=None,dsloaisach=dsloaisach) 
            else:                      
                s = sach(tensach=tensach,maloai=maloai,tenloaisach=tl,tacgia=tacgia,nhaxuatban=nhaxuatban,soluong=soluong,gia=gia)
                db.session.add(s)  
                db.session.commit()
                session['themsach'] = 1
                return redirect('/sach')
        return render_template('formsach.html', dsloaisach=dsloaisach, sach=None)
    return render_template('index.html')
@app.route('/capnhatsach/<masach>', methods=["get","post"])
def capnhatsach(masach):
    if current_user.is_authenticated:
        dsloaisach  = loaisach.query.all()
        if request.method == "POST":
            tensach = request.form.get("tensach")
            tensachcu = request.form.get("tensachcu")
            tacgia = request.form.get("tacgia")
            nhaxuatban = request.form.get("nhaxuatban")
            soluong = request.form.get("soluong")
            gia = request.form.get("gia")
            maloai = request.form.get("maloai")
            dssach = sach.query.where(sach.tensach==tensach).all()
            sachcu = sach.query.filter(sach.masach==masach).first()
            if (tensach!=tensachcu):
                # Kiểm tra trùng tên  sách
                dssach = sach.query.where(sach.tensach==tensach).all()
                if len(dssach) > 0:
                    return render_template('formsach.html',trungten=1,dsloaisach=dsloaisach,sach=sachcu) 
            s = sach.query.filter(sach.masach==masach).first()
            s.tensach = tensach
            s.tacgia = tacgia
            s.nhaxuatban = nhaxuatban
            s.soluong = soluong
            s.gia = gia
            s.maloai = maloai
            ls = loaisach.query.filter(loaisach.maloai==maloai).first()
            s.tenloaisach = ls.tenloai
            db.session.commit()
            session['capnhatsach'] = 1
            return redirect('/sach')

        s_ach = sach.query.filter(sach.masach==masach).first()
        return render_template('formsach.html',sach=s_ach,dsloaisach=dsloaisach)
    return render_template('index.html')
@app.route('/xoasach/<masach>', methods=["get","post"])
def xoasach(masach):
    if current_user.is_authenticated:
        s = sach.query.filter(sach.masach==masach).first()
        dsdonmuon = donmuon.query.filter(donmuon.masach==masach).all()
        for don in dsdonmuon:
            db.session.delete(don)
        db.session.delete(s)
        db.session.commit()
        session['xoasach'] = 1
        return redirect('/sach')
    return render_template('index.html')

# Đơn mượn
@app.route('/donmuon', methods=["get","post"])
def ds_donmuon():
    if current_user.is_authenticated:
        today = date.today()
        dsdonquahan = donmuon.query.filter(donmuon.hantra<today,donmuon.trangthai=="Chưa trả").all()
        for don in dsdonquahan:
            don.trangthai = "Quá hạn"
        db.session.commit()
        key = request.form.get("key")
        dsdonmuon = donmuon.query.all()
        
        if key != None:
            if key != "":
                dsdonmuon = donmuon.query.filter(donmuon.masv.like('%'+key+'%')|donmuon.hoten.like('%'+key+'%')|donmuon.tensach.like('%'+key+'%')).all()
            else:
                dsdonmuon = []
        themdon = None
        xoadon = None
        capnhatdon = None    
        trasach = None
        dangmuonsach = None
        if 'themdon' in session:
            themdon = 1
            session.pop('themdon',None)
        if 'xoadon' in session:
            xoadon = 1
            session.pop('xoadon',None)
        if 'capnhatdon' in session:
            capnhatdon = 1
            session.pop('capnhatdon',None)
        if 'trasach' in session:
            trasach = 1
            session.pop('trasach',None)
        if 'dangmuonsach' in session:
            dangmuonsach = 1
            session.pop('dangmuonsach',None)
        return render_template('donmuon.html',dsdonmuon=dsdonmuon,themdon=themdon,xoadon=xoadon,capnhatdon=capnhatdon,trasach=trasach,dangmuonsach=dangmuonsach)
    return render_template('index.html')

@app.route('/themdonmuon', methods=["get","post"])
def themdonmuon():
    if current_user.is_authenticated:
        dssach  = sach.query.all()
        if request.method == "POST":
            masv = request.form.get("masv")
            masach = request.form.get("masach")
            ngaymuon = request.form.get("ngaymuon")
            hantra = request.form.get("hantra")
            sv = sinhvien.query.filter(sinhvien.masv==masv).first()
            s = sach.query.filter(sach.masach==masach).first()
            ngaymuon = date.fromisoformat(ngaymuon)
            hantra = date.fromisoformat(hantra)
            trangthai= "Chưa trả"
            if sv == None:
                return render_template('formdonmuon.html', dssach=dssach, donmuon=None,khongcosv=1)
            else:
                donmuonsach = donmuon(masv=masv,hoten=sv.hoten,masach=masach,tensach=s.tensach,ngaymuon=ngaymuon,hantra=hantra,trangthai=trangthai)
                dsdonmuon_sv = donmuon.query.filter(donmuon.masv==masv,donmuon.trangthai!="Đã trả").all()
                if len(dsdonmuon_sv) > 0:
                    session['dangmuonsach']=1
                    return redirect('/donmuon')
                # kiem tra so luong sach
                kt_sach = sach.query.filter(sach.masach==masach).first()    
                if kt_sach.soluong == 0:
                    return render_template('formdonmuon.html', dssach=dssach, donmuon=None,hetsach=1)

                db.session.add(donmuonsach)  
                kt_sach.soluong -= 1
                db.session.commit()
                session['themdon'] = 1
                return redirect('/donmuon')
        return render_template('formdonmuon.html', dssach=dssach, donmuon=None)
    return render_template('index.html')
@app.route('/capnhatdonmuon/<madonmuon>', methods=["get","post"])
def capnhatdonmuon(madonmuon):
    if current_user.is_authenticated:
        list_trangthai = ["Chưa trả","Đã trả","Quá hạn"]
        dssach  = sach.query.all()
        if request.method == "POST":
            masv = request.form.get("masv")
            masach = request.form.get("masach")
            masachcu = request.form.get("masachcu")
            ngaymuon = request.form.get("ngaymuon")
            hantra = request.form.get("hantra")
            sv = sinhvien.query.filter(sinhvien.masv==masv).first()
            s = sach.query.filter(sach.masach==masach).first()
            ngaymuon = date.fromisoformat(ngaymuon)
            hantra = date.fromisoformat(hantra)
            trangthai= request.form.get("trangthai")
            trangthaicu= request.form.get("trangthaicu")
            dsdonmuon_sv = donmuon.query.filter(donmuon.masv==masv,donmuon.trangthai!="Đã trả").all()
            donmuonsach = donmuon.query.filter(donmuon.madonmuon==madonmuon).first()

            if donmuonsach.trangthai != "Đã trả":
                pass
            elif len(dsdonmuon_sv) > 0:
                session['dangmuonsach']=1
                return redirect('/donmuon')
            # Xử lí số lượng sách khi cập nhật
            if masach == masachcu:
                sach_1 = sach.query.filter(sach.masach==masach).first()
                if trangthaicu != "Đã trả" and trangthai == "Đã trả":
                    sach_1.soluong += 1
                if trangthai != "Đã trả" and trangthaicu == "Đã trả":
                    if sach_1.soluong == 0:
                        return render_template('formdonmuon.html',donmuon=donmuonsach,dssach=dssach, trangthai=list_trangthai,hetsach=1)
                    sach_1.soluong -= 1
                db.session.commit()
            else:
                sach_1 = sach.query.filter(sach.masach==masachcu).first()
                sach_2 = sach.query.filter(sach.masach==masach).first()
                if trangthaicu != "Đã trả":
                    sach_1.soluong += 1
                    if trangthai == "Đã trả":
                        pass
                    else:
                        if sach_2.soluong == 0:
                            return render_template('formdonmuon.html',donmuon=donmuonsach,dssach=dssach, trangthai=list_trangthai,hetsach=1)
                
                if trangthai != "Đã trả":
                    if sach_2.soluong == 0:
                        return render_template('formdonmuon.html',donmuon=donmuonsach,dssach=dssach, trangthai=list_trangthai,hetsach=1)
                    sach_2.soluong -= 1
                db.session.commit()

            donmuonsach.masv = masv
            donmuonsach.masach = masach
            donmuonsach.hoten = sv.hoten
            donmuonsach.tensach = s.tensach
            donmuonsach.ngaymuon = ngaymuon
            donmuonsach.hantra = hantra
            donmuonsach.trangthai = trangthai
            db.session.commit()
            session['capnhatdon'] = 1
            return redirect('/donmuon')
        donmuonsach = donmuon.query.filter(donmuon.madonmuon==madonmuon).first()
        return render_template('formdonmuon.html',donmuon=donmuonsach,dssach=dssach, trangthai=list_trangthai)
    return render_template('index.html')
@app.route('/xoadonmuon/<madonmuon>', methods=["get","post"])
def xoadonmuon(madonmuon):
    if current_user.is_authenticated:
        donmuonsach = donmuon.query.filter(donmuon.madonmuon==madonmuon).first()
        if donmuonsach.trangthai != "Đã trả":
            s = sach.query.filter(sach.masach==donmuonsach.masach).first()
            s.soluong += 1
        db.session.delete(donmuonsach)
        db.session.commit()
        session['xoadon'] = 1
        return redirect('/donmuon')
    return render_template('index.html')
@app.route('/trasach/<madonmuon>', methods=["get","post"])
def trasach(madonmuon):
    if current_user.is_authenticated:
        donmuonsach = donmuon.query.filter(donmuon.madonmuon==madonmuon).first()
        s = sach.query.filter(sach.masach==donmuonsach.masach).first()
        s.soluong += 1
        donmuonsach.trangthai = "Đã trả"
        db.session.commit()
        session['trasach'] = 1
        return redirect('/donmuon')
    return render_template('index.html')