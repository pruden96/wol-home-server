from flask import Blueprint, request, jsonify
from wakeonlan import send_magic_packet
from models import get_mac_by_tag

wol_bp = Blueprint('wol', __name__)

@wol_bp.route('/wake', methods=['POST'])
def wake():
    # auth = request.args.get("auth")
    # if auth != AUTH_KEY:
    #     return jsonify({"status": "error", "message": "Autenticación fallida"}), 403

    device = request.args.get("tag")
    if not device:
        return jsonify({"status": "error", "message": "Se requiere el parámetro 'tag'."}), 400
    
    device_name = request.args.get("name")
    if not device_name:
        return jsonify({"status": "error", "message": "Se requiere el parámetro 'name'."}), 400
    
    device_mac = get_mac_by_tag(device)
    if not device_mac:
        return jsonify({"status": "error", "message": "MAC no encontrada"}), 404

    try:
        send_magic_packet(device_mac)
        return jsonify({"status": "success", "message": f"Packet WOL enviado a {device_name} ({device_mac})"}), 200
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500