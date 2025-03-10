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
from flask_jwt_extended import get_jwt, get_jwt_identity, jwt_required

from models import (
    get_device_ip,
    get_device_mac,
    get_device_tag,
    get_devices_by_userid,
    insert_device,
    remove_device_by_tag,
    update_device_name_by_tag,
)

device_bp = Blueprint("device", __name__)


# Ruta para dashboard
@device_bp.route("/")
@jwt_required()
def dashboard() -> str:
    user_id = get_jwt_identity()  # Obtiene el user_id
    user_role = get_jwt()["role"]  # Obtiene el role desde los claims (payload)
    devices = get_devices_by_userid(user_id)
    response = make_response(
        render_template("index.html", devices=devices, role=user_role)
    )

    # Deshabilitar la caché para evitar que el navegador almacene esta página
    response.headers["Cache-Control"] = (
        "no-store, no-cache, must-revalidate, proxy-revalidate"
    )
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"

    return response
    # return render_template("index.html", devices=devices, role=user_role)


# Ruta para agregar un dispositivo
@device_bp.route("/add_device", methods=["GET", "POST"])
@jwt_required()
def add_device() -> str | Response:
    name = None
    mac = None
    ip = None

    user_role = get_jwt()["role"]  # Obtiene el role desde los claims (payload)

    if request.method == "POST":
        data = request.get_json()
        if data is None:
            return jsonify({"error": "No se proporcionaron datos JSON"}), 400

        name = data.get("name")
        tag = data.get("tag")
        mac = data.get("mac")
        if mac == "none":
            mac = None
        ip = data.get("ip")
        if ip == "none":
            ip = None
        type = data.get("type")
        user_id = get_jwt_identity()  # Obtiene el user_id

        tag_fetched = get_device_tag(tag)
        # Verificar que el tag esté permitido (debe ser uno de los tags predefinidos)
        if tag_fetched is not None:
            # print('tag repetido')
            return jsonify({"error_tag": "Tag en uso. Seleccione otro"}), 400

        mac_fetched = get_device_mac(mac, user_id)
        if mac_fetched is not None:
            # print('mac repetido')
            return jsonify({"error_mac": "MAC en uso. Seleccione otro"}), 400

        ip_fetched = get_device_ip(ip, user_id)
        if ip_fetched is not None:
            # print('ip repetido')
            return jsonify({"error_ip": "IP en uso. Seleccione otro"}), 400

        # Insertar dispositivo en la base de datos
        insert_device(user_id, name, tag, type, mac=mac, ip=ip)
        return redirect(url_for("device.dashboard"))

    return render_template("add_device.html", name=name, mac=mac, ip=ip, role=user_role)


@device_bp.route("/remove_device", methods=["DELETE"])
@jwt_required()
def remove_device() -> Response:
    name = request.args.get("name")
    tag = request.args.get("tag")
    if name is None or tag is None:
        return jsonify({"error": "No se proporcionaron datos JSON"}), 400

    remove_device_by_tag(tag)
    return "", 204


@device_bp.route("/update_device_name", methods=["PUT"])
@jwt_required()
def update_device_name() -> Response:
    data = request.get_json()
    if data is None:
        return jsonify({"error": "No se proporcionaron datos JSON"}), 400
    name = data.get("name")
    tag = data.get("tag")
    if name is None or tag is None:
        return jsonify({"error_tag_name": "Name or Tag missing"}), 400
    # print(f"Name: {name}, Tag: {tag}")
    update_device_name_by_tag(tag, name)
    return jsonify({"success": True}), 200
