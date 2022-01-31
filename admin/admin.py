from flask import Blueprint, request, redirect, render_template, url_for, flash, session

admin = Blueprint('admin', __name__, template_folder='templates', static_folder='static')

def login_admin():
    session['admin_logged'] = 1
    
def isLogged():
    return True if session.get('admin_logged') else False

def logout_admin():
    session.pop('admin_logged', None)

menu = [{'url': '.index', 'title': 'Panel'},
        {'url': '.logout', 'title': 'Logout'}]

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
