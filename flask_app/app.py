from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = "clave_secreta"  # Cambia esto por una clave segura

# Simulamos una base de datos de usuarios
users = {
    "usuario1": generate_password_hash("password1"),
    "usuario2": generate_password_hash("password2")
}

@app.route("/")
def home():
    if "username" in session:
        return f"Bienvenido, {session['username']}! <a href='/logout'>Cerrar sesión</a>"
    return "Bienvenido! <a href='/login'>Inicia sesión</a>"

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        # Verifica si el usuario existe y la contraseña es correcta
        if username in users and check_password_hash(users[username], password):
            session["username"] = username
            flash("Inicio de sesión exitoso", "success")
            return redirect(url_for("home"))
        else:
            flash("Usuario o contraseña incorrectos", "danger")

    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("username", None)
    flash("Has cerrado sesión", "info")
    return redirect(url_for("home"))

if __name__ == "__main__":
    app.run(debug=True)
