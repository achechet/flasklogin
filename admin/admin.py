import sqlite3
from flask import Blueprint, request, redirect, render_template, url_for, flash, session, g

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

def login_admin():
    session['admin_logged'] = 1
    
def isLogged():
    return True if session.get('admin_logged') else False

def logout_admin():
    session.pop('admin_logged', None)

menu = [{'url': '.index', 'title': 'Panel'},
        {'url': '.listusers', 'title': 'Спсиок пользователей'},
        {'url': '.logout', 'title': 'Logout'}]

db = None
@admin.before_request
def before_request():
    global db 
    db = g.get('link_db')
    
@admin.teardown_request
def teardown_request(request):
    global db 
    db = None
    return request    

@admin.route('/')
def index():
    if not isLogged():
        return redirect(url_for('.index'))
    
    return render_template('admin/index.html', menu=menu, title='Admin-Panel')

@admin.route('/login', methods=['POST', "GET"])
def login():
    if isLogged():
        return redirect(url_for('.index'))
    
    if request.method == "POST":
        if request.form['user'] == "admin" and request.form['psw'] == "1234":
            login_admin()
            return redirect(url_for('.index'))
        else:
            flash("Неверная пара login/password", "error") 

    return render_template('admin/login.html', title='Admin-Panel')

@admin.route('/logout', methods=['POST', "GET"])
def logout():
    if not isLogged():
        return redirect(url_for('.login'))
    
    logout_admin()
    
    return redirect(url_for('.login'))

@admin.route('list-users')
def listusers():
    if not isLogged():
        return redirect(url_for('.login'))
    
    list = []
    if db:
        try:
            cur = db.cursor()
            cur.execute(f"SELECT name, email FROM users ORDER BY time DESC")
            list = cur.fetchall()            
        except sqlite3.Error as e:
            print("Ошибка получения статей из БД "+str(e))
    
    return render_template('admin/listusers.html', title='Список пользователей', menu=menu, list=list)                        
