from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, RegistroUsuario

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mi_secreto'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/flask_app'


db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return RegistroUsuario.query.get(int(user_id))

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
        # Cambiar 'username' por 'departamento_id' para reflejar el formulario actualizado
        departamento_id = request.form.get('departamento_id')  # Captura el ID del departamento
        password = request.form.get('password')  # Captura la contraseña
        
        if not departamento_id or not password:
            flash("Por favor, llena todos los campos.")
            return render_template('login.html')
        
        # Busca al departamento en la base de datos
        departamento = departamento_id.query.filter_by(ID=departamento_id).first()
        
        if departamento and departamento.Contraseña == password:
            # Autenticación exitosa, redirigir al menú o dashboard
            flash("¡Inicio de sesión exitoso!")
            return redirect(url_for('menu'))
        else:
            flash("ID de Departamento o contraseña incorrectos.")
    
    return render_template('login.html')




@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        departamento_id = request.form['departamento_id']
        password = request.form['password']
        
        if RegistroUsuario.query.filter_by(DepartamentoID=departamento_id).first():
            flash('El ID de departamento ya está en uso')
        else:
            user = RegistroUsuario(
                Nombre=first_name,
                Apellidos=last_name,
                Email=email,
                DepartamentoID=departamento_id,
                Contraseña=generate_password_hash(password)
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

@app.route('/formulario_Subdirec') 
@login_required
def formulario_Subdirec(): 
    return render_template('formulario_Subdirec.html')

@app.route('/formcuidadoinfacias') 
@login_required
def formcuidadoinfancias(): 
    return render_template('formcuidadoinfancias.html')

if __name__ == '__main__':
    app.run(debug=True)
