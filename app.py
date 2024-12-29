from flask import Flask, render_template, redirect, url_for, request, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, RegistroUsuario, Departamento

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
        # Captura los datos del formulario
        departamento_nombre = request.form.get('departamento')
        password = request.form.get('password')

        # Verifica que los campos no estén vacíos
        if not departamento_nombre or not password:
            flash("Por favor, llena todos los campos.")
            return render_template('login.html')
        
        # Busca el departamento por nombre
        departamento = Departamento.query.filter_by(Departamento=departamento_nombre).first()
        
        # Verifica la contraseña
        if departamento and departamento.Contraseña == password:
            flash("¡Inicio de sesión exitoso!")
            return redirect(url_for('menu'))  # Cambia 'menu' por tu ruta principal si es necesario
        else:
            flash("Nombre de Departamento o contraseña incorrectos.")
    
    return render_template('login.html')






@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Captura los datos del formulario
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        departamento_nombre = request.form['departamento_nombre']
        password = request.form['password']
        
        # Busca el departamento por nombre
        departamento = Departamento.query.filter_by(Departamento=departamento_nombre).first()
        if not departamento:
            flash('El departamento ingresado no existe. Por favor, verifica el nombre.')
            return render_template('register.html')
        
        # Verifica si el departamento ya está registrado con un usuario
        if RegistroUsuario.query.filter_by(DepartamentoID=departamento.ID).first():
            flash('El departamento ya está asignado a otro usuario.')
            return render_template('register.html')
        
        # Verifica si el correo ya está registrado
        if RegistroUsuario.query.filter_by(Email=email).first():
            flash('El correo electrónico ya está registrado.')
            return render_template('register.html')

        # Crea un nuevo usuario
        user = RegistroUsuario(
            Nombre=first_name,
            Apellidos=last_name,
            Email=email,
            DepartamentoID=departamento.ID,  # Asocia el ID del departamento
            Contraseña=generate_password_hash(password)  # Hash seguro de la contraseña
        )
        db.session.add(user)
        db.session.commit()
        flash('Registro exitoso, ahora puedes iniciar sesión.')
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
