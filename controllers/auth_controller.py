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
    unset_jwt_cookies,
    verify_jwt_in_request,
)

from models import get_user_login

auth_bp = Blueprint("auth", __name__)


def current_user_is_authenticated():
    try:
        verify_jwt_in_request()  # Verificar que el token sea válido
        user_identity = get_jwt_identity()  # Obtener el usuario del token  # noqa: F841
        return user_identity is not None  # Token válido, usuario autenticado
    except Exception:
        return False  # Token inválido o expirado


# Ruta para inicio de sesión
@auth_bp.route("/login", methods=["GET", "POST"])
def login() -> str | Response:
    if current_user_is_authenticated():  # Si el usuario ya tiene un JWT válido
        return redirect(url_for("device.dashboard"))

    if request.method == "POST":
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No se proporcionaron datos JSON"}), 400

        username = data.get("username")
        password = data.get("password")

        user = get_user_login(username, password)
        if user:
            # Crea el token con los detalles del usuario como parte del payload
            access_token = create_access_token(
                identity=str(
                    user["id"]
                ),  # Usamos el user_id como identidad, debe ser string
                expires_delta=timedelta(hours=1),  # Expira en 1 hora
                additional_claims={"role": user["role"]},  # Agregamos el rol al payload
            )
            print("Log in correcto")
            response = make_response(
                jsonify(
                    {
                        "message": "Login exitoso",
                        "redirect_url": url_for("device.dashboard"),
                    }
                )
            )
            response.set_cookie(
                "access_token",
                access_token,
                httponly=True,
                secure=False,
                samesite="Lax",
            )

            return response
        else:
            return jsonify({"error_auth": "Credenciales incorrectas"}), 401

    return render_template("login.html")


@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout() -> Response:
    response = make_response(
        jsonify({"message": "Logout exitoso", "redirect_url": url_for("auth.login")})
    )
    response.status_code = 200
    unset_jwt_cookies(response)
    return response


@auth_bp.route("/api/validate-token", methods=["GET"])
def validate_token() -> Response:
    try:
        verify_jwt_in_request()  # Verificar que el token sea válido
        user_identity = get_jwt_identity()  # Obtener el usuario del token
        return jsonify({"user_identity": user_identity}), 200
    except Exception:
        return jsonify({"error": "Token inválido o expirado"}), 401
