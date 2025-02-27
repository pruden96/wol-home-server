from flask import (
    Blueprint,
    Response,
    jsonify,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from models import get_user_login

auth_bp = Blueprint("auth", __name__)


# Ruta para inicio de sesión (autenticación básica)
@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    if request.method == "POST":
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No se proporcionaron datos JSON"}), 400

        username = data.get("username")
        password = data.get("password")

        user = get_user_login(username, password)
        if user:
            session["user_id"] = user["id"]
            session["role"] = user["role"]
            return redirect(url_for("device.dashboard"))
        else:
            return jsonify({"error_auth": "Credenciales incorrectas"}), 401
    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
def logout() -> Response:
    if "user_id" not in session:
        return jsonify({"error": "No hay sesión activa"}), 401

    session.pop("user_id", None)
    session.clear()
    response = redirect(url_for("auth.login"))
    response.delete_cookie("session")  # El nombre de la cookie de sesión
    return response
