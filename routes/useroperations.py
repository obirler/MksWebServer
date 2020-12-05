from flask import request, jsonify, render_template
from flask_login import login_user, login_required, logout_user
from config import app, login_manager, DbPath, ADMIN_PASSWORD, ADMIN_NAME, ADMIN_USER_NAME, ADMIN_SURNAME
from werkzeug.security import check_password_hash
from models import User
import dbexecutor
import util
import os


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        surname = request.form['surname']
        user = User.query.filter_by(username=username).first()
        if not user:
            if len(username) < 4:
                return jsonify(responsecode=-1, message="Kullanıcı adı en az 4 karakter olmalı!")
            if len(password) < 4:
                return jsonify(responsecode=-2, message="Şifre en az 4 karakter olmalı!")
            if len(name) < 1:
                return jsonify(responsecode=-3, message="Lütfen adınızı giriniz!")
            if len(surname) < 1:
                return jsonify(responsecode=-4, message="Lütfen soyadınızı giriniz!")

            dbexecutor.addUser(username, name, surname, password, False)

            return jsonify(responsecode=0, heading="Tebrikler!", message="Sisteme başarıyla kayıt oldunuz.",
                           postmessage="Şimdi giriş yapma sayfasına yönlendirileceksiniz.")
        else:
            return jsonify(responsecode=-5, message="Bu kullanıcı adı alınmış! Başka bir kullanıcı adı girin.")
    elif request.method == 'GET':
        return render_template("signup.html", message="")


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if len(username) < 1:
            return jsonify(responsecode=-3, message="Lütfen kullanıcı adını giriniz!")
        if len(password) < 1:
            return jsonify(responsecode=-4, message="Lütfen şifreyi giriniz!")

        user = User.query.filter_by(username=username).first()
        if user:
            if check_password_hash(user.password, password):
                login_user(user)
                util.setUserSession(user)
                return jsonify(responsecode=0, heading="Tebrikler!", message="Sisteme başarıyla giriş yaptınız.",
                               postmessage="Şimdi ana sayfaya yönlendirileceksiniz.")
            else:
                return jsonify(responsecode=-1, message="Şifre yanlış!")
        else:
            return jsonify(responsecode=-2, message="Bu isimde bir kullanıcı yoktur!")
    elif request.method == 'GET':
        return render_template("login.html")


@app.route('/logout', methods=['GET'])
@login_required
def logout():
    logout_user()
    util.deleteSession()
    return render_template("logout.html")


@app.route('/userprofile', methods=['GET'])
@login_required
def userprofile():
    return render_template("userprofile.html")


@app.route('/userprofile/namechange', methods=['POST'])
@login_required
def changename():
    id = request.form['id']
    newname = request.form['newname']
    if len(newname) < 1:
        return jsonify(responsecode=-1, message="Lütfen adınızı giriniz!")
    user = dbexecutor.getUser(id)
    if user:
        user.name = newname
        user.setChanged()
        dbexecutor.commit()
        util.setUserSession(user)
        return jsonify(responsecode=0)
    else:
        return jsonify(responsecode=-2, message="Böyle bir kullanıcı yok!")


@app.route('/userprofile/surnamechange', methods=['POST'])
@login_required
def changesurname():
    id = request.form['id']
    newsurname = request.form['newsurname']
    if len(newsurname) < 1:
        return jsonify(responsecode=-1, message="Lütfen soyadınızı giriniz!")
    user = User.query.filter_by(id=id).first()
    if user:
        user.surname = newsurname
        user.setChanged()
        dbexecutor.commit()
        util.setUserSession(user)
        return jsonify(responsecode=0)
    else:
        return jsonify(responsecode=-2, message="Böyle bir kullanıcı yok!")


@app.route('/userprofile/usernamechange', methods=['POST'])
@login_required
def changeusername():
    id = request.form['id']
    newusername = request.form['newusername']
    if len(newusername) < 1:
        return jsonify(responsecode=-1, message="Lütfen kullanıcı adınızı giriniz!")

    if len(newusername) < 4:
        return jsonify(responsecode=-2, message="Kullanıcı adı en az 4 karakter olmalı!")

    user = dbexecutor.getUser(id)
    if user:
        useralike = dbexecutor.getUserByUserName(newusername)
        if useralike in None:
            return jsonify(responsecode=-3, message="Bu kullanıcı adı alınmış!")
        else:
            if dbexecutor.updateUser(id, newusername, user.name, user.surname, user.password,
                                     user.isadmin, True) is not None:
                util.setUserSession(user)
            return jsonify(responsecode=0)
    else:
        return jsonify(responsecode=-4, message="Böyle bir kullanıcı yok!")


@app.route('/users', methods=['GET'])
@login_required
def users():
    users = dbexecutor.getAllUsers()
    return render_template("users.html", users=users)

@app.route('/userprofile/passwordchange', methods=['POST'])
@login_required
def changepassword():
    id = request.form['id']
    newpassword1 = request.form['newpassword1']
    newpassword2 = request.form['newpassword2']
    if len(newpassword1) < 1:
        return jsonify(responsecode=-1, message="Lütfen şifrenizi giriniz!")
    if len(newpassword1) < 4:
        return jsonify(responsecode=-2, message="Şifre en az 4 karakter olmalı!")
    if len(newpassword2) < 1:
        return jsonify(responsecode=-3, message="Lütfen şifrenizi doğrulayınız!")
    if newpassword1 != newpassword2:
        return jsonify(responsecode=-4, message="Girilen şifreler farklı!")

    user = dbexecutor.getUser(id)

    if user:
        if dbexecutor.updateUser(id, user.username, user.name, user.surname, newpassword1,
                                 user.isadmin, True) is not None:
            util.setUserSession(user)
            return jsonify(responsecode=0)
        else:
            return jsonify(responsecode=-1, message="Şifre Değiştirilemedi")
    else:
        return jsonify(responsecode=-5, message="Böyle bir kullanıcı yok!")


def registeradmin():
    user = User.query.filter_by(isadmin=True).first()
    if not user:
        dbexecutor.addUser(ADMIN_USER_NAME, ADMIN_NAME, ADMIN_SURNAME, ADMIN_PASSWORD, True)
