import logging
from datetime import timedelta

from flask import (
    Blueprint,
    Response,
    jsonify,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
from flask_jwt_extended import (
    create_access_token,
    get_jwt_identity,
    jwt_required,
    set_access_cookies,
    unset_jwt_cookies,
    verify_jwt_in_request,
)

from models import get_user_login

auth_bp = Blueprint("auth", __name__)


def current_user_is_authenticated():
    try:
        verify_jwt_in_request()
        user_identity = (  # noqa: F841
            get_jwt_identity()
        )  # Devuelve la identidad del payload del JWT
        return True
    except Exception:
        # print(e)
        # print("No se pudo verificar el token")
        return False


# Ruta para inicio de sesión (autenticación JWT)
@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    if current_user_is_authenticated():  # Si el usuario ya tiene un JWT válido
        logging.info("Ejecutando logout")
        # Respuesta para renderizar el login sin token
        response = make_response(render_template("login.html"))
        # Borrar la cookie del JWT sin redirigir a logout
        unset_jwt_cookies(response)

        return response

    if request.method == "POST":
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No se proporcionaron datos JSON"}), 400

        username = data.get("username")
        password = data.get("password")

        user = get_user_login(username, password)
        if user:
            # Usamos el user_id como la identidad del token (string)
            identity = str(user["id"])  # DEBE SER STRING
            # Crea el token con los detalles del usuario como parte del payload
            access_token = create_access_token(
                identity=identity,  # Usamos el user_id como identidad
                expires_delta=timedelta(hours=1),  # Expira en 1 hora
                additional_claims={"role": user["role"]},  # Agregamos el rol al payload
            )

            response = make_response(
                redirect(url_for("device.dashboard"))
            )  # Crear respuesta HTTP
            set_access_cookies(response, access_token)  # Almacena el token en la cookie

            return response  # Retorna la respuesta con la cookie configurada
        else:
            return jsonify({"error_auth": "Credenciales incorrectas"}), 401

    response = make_response(render_template("login.html"))

    # Deshabilitar la caché para evitar que el navegador almacene esta página
    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, proxy-revalidate"
    )
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout() -> Response:
    response = redirect(url_for("auth.login"))
    unset_jwt_cookies(response)  # Borra la cookie del token

    return response
