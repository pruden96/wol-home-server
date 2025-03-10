from flask import (
    Blueprint,
    Response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_jwt_extended import get_jwt, jwt_required

from models import insert_new_user
from validators.user_validators import (
    is_email_taken,
    is_username_taken,
    validate_email,
    validate_username,
)

user_bp = Blueprint("user", __name__)


@user_bp.route("/register", methods=["GET", "POST"])
@jwt_required()
def register() -> str | Response:
    user_role = get_jwt()["role"] # Obtiene el role desde los claims (payload)

    if user_role != "admin":
        return redirect(url_for("device.dashboard"))

    if request.method == "POST":
        error_user = ""
        error_email = ""
        error_pwd = ""

        form_validation = True
        db_validation = True

        username = request.form.get("new-username")
        password = request.form.get("new-pwd")
        confirm_password = request.form.get("new-conf-pwd")
        email = request.form.get("new-email")

        if password != confirm_password:
            error_pwd = "Las contraseñas no coinciden"
            form_validation = False

        if not validate_username(username):
            error_user = "Nombre de usuario no válido. Longitud debe ser 4 a 20 caracteres alfanuméricos"
            form_validation = False

        if not validate_email(email):
            error_email = "Correo electrónico no válido"
            form_validation = False

        if not form_validation:
            return render_template(
                "register.html",
                error_user=error_user,
                error_email=error_email,
                error_pwd=error_pwd,
            ), 400

        if is_username_taken(username):
            error_user = "Nombre de usuario en uso"
            db_validation = False

        if is_email_taken(email):
            error_email = "Correo electrónico en uso"
            db_validation = False

        if not db_validation:
            return render_template(
                "register.html",
                error_user=error_user,
                error_email=error_email,
                error_pwd="",
            ), 400

        insert_new_user(username, password, email)

        # Aquí puedes agregar la lógica para guardar el usuario en la base de datos
        # Por ejemplo, puedes llamar a una función que realice la inserción en la base de datos

        return redirect(url_for("device.dashboard"))

    return render_template("register.html")
