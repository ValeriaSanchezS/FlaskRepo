from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_secreto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def before_request():
    if not hasattr(app, 'db_initialized'):
        db.create_all()
        app.db_initialized = True

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and user.verify_password(password):
            login_user(user)
            return redirect(url_for('menu'))
        flash('Nombre de usuario o contraseña incorrectos')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        department = request.form['department']
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('El nombre de usuario ya está en uso')
        else:
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                department=department,
                username=username,
                password_hash=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
            flash('Registro exitoso, ahora puedes iniciar sesión')
            return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/menu')
@login_required
def menu():
    return render_template('menu.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/datos')
@login_required
def datos():
    return render_template('form.html')

@app.route('/metas')
@login_required
def metas():
    return render_template('metas.html')

@app.route('/progreso')
@login_required
def progreso():
    return render_template('progreso.html')

@app.route('/graficas')
@login_required
def graficas():
    return render_template('graficas.html')


@app.route('/configuracion')
@login_required
def configuracion():
    return render_template('configuracion.html')

#FORMULARIOS

# Definir el nuevo endpoint para el formulario
@app.route('/form')
@login_required
def form():
    return render_template('form.html')

@app.route('/formapoyo') 
@login_required
def formapoyo(): 
    return render_template('formapoyo.html')

@app.route('/formtransfor') 
@login_required
def formtransfor(): 
    return render_template('formtransfor.html')

@app.route('/formjuven') 
@login_required
def formjuven(): 
    return render_template('formjuven.html')

if __name__ == '__main__':
    app.run(debug=True)
