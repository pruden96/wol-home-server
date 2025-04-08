import os
import sys

from flask import (
    Blueprint,
    Response,
    jsonify,
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

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from config import Config

device_bp = Blueprint("device", __name__)
PING_PARAM = Config.PING_PARAM


# Ruta GET para renderizar el dashboard
@device_bp.route("/", methods=["GET"])
@jwt_required()
def dashboard() -> str:
    user_id = get_jwt_identity()  # Obtiene el user_id
    user_role = get_jwt()["role"]  # Obtiene el role desde los claims (payload)
    devices = get_devices_by_userid(user_id)

    return render_template("index.html", devices=devices, role=user_role)


# Ruta GET para renderizar el formulario de agregar dispositivo
@device_bp.route("/add_device", methods=["GET"])
@jwt_required()
def render_add_device() -> str:
    name = None
    mac = None
    ip = None
    user_role = get_jwt()["role"]  # Obtiene el role desde los claims (payload)
    return render_template("add_device.html", name=name, mac=mac, ip=ip, role=user_role)


# Ruta POST para agregar un dispositivo
@device_bp.route("/add_device", methods=["POST"])
@jwt_required()
def add_device() -> str | Response:
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


# Ruta DELETE para eliminar un dispositivo
@device_bp.route("/remove_device", methods=["DELETE"])
@jwt_required()
def remove_device() -> Response:
    name = request.args.get("name")
    tag = request.args.get("tag")
    if name is None or tag is None:
        return jsonify({"error": "No se proporcionaron datos JSON"}), 400

    remove_device_by_tag(tag)
    return "", 204


# Ruta PUT para actualizar el nombre de un dispositivo
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

def can_ping(ip_address: str) -> bool:
    """
    Intenta hacer ping a una dirección IP.

    Args:
        ip_address (str): La dirección IP a la que hacer ping.

    Returns:
        bool: True si el ping es exitoso, False en caso contrario.
    """
    import subprocess

    command = ['ping', PING_PARAM, '1', ip_address]

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=2)
        return result.returncode == 0
    except subprocess.TimeoutExpired:
        return False
    except subprocess.CalledProcessError:
        return False
    except OSError as e:
        print(f"Error al ejecutar el comando ping: {e}")
        return False

# Ruta GET para obtener el estado [ON-OFF] de un dispositivo WoL
@device_bp.route("/device-status", methods=["GET"])
@jwt_required()
def ping_device() -> Response:
    user_id = get_jwt_identity()
    devices = get_devices_by_userid(user_id)
    response = { device["tag"]: can_ping(device["ip"]) for device in devices if device["ip"] and device["type"] == "wol" }
    print(response)
    return jsonify(response), 200
