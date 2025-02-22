from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from models import get_devices_by_userid, insert_device, get_all_tags, remove_device_by_tag, update_device_name_by_tag, get_device_tag, get_device_mac, get_device_ip
from validators.device_validator import validate_device_name, validate_device_tag
import logging


device_bp = Blueprint('device', __name__)

# Ruta para dashboard
@device_bp.route('/')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    
    user_id = session['user_id']
    user_role = session['role']
    devices = get_devices_by_userid(user_id)
    return render_template('index.html', devices=devices, role=user_role)

# Ruta para agregar un dispositivo
@device_bp.route('/add_device', methods=['GET', 'POST'])
def add_device():
    name = None
    mac = None
    ip = None

    if 'user_id' not in session:
        return redirect(url_for('auth.login'))
    user_role = session['role']

    if request.method == 'POST':
        
        data = request.get_json()
        if data is None:
            return jsonify({'error': 'No se proporcionaron datos JSON'}), 400

        name = data.get('name')
        tag = data.get('tag')
        mac = data.get('mac')
        if mac == 'none':
            mac = None
        ip = data.get('ip')
        if ip == 'none':
            ip = None
        type = data.get('type')
        user_id = session['user_id']

        tag_fetched = get_device_tag(tag)
        # Verificar que el tag esté permitido (debe ser uno de los tags predefinidos)
        if tag_fetched is not None:
            # print('tag repetido')
            return jsonify({'error_tag': 'Tag en uso. Seleccione otro'}), 400
        
        mac_fetched = get_device_mac(mac, user_id)
        if mac_fetched is not None:
            # print('mac repetido')
            return jsonify({'error_mac': 'MAC en uso. Seleccione otro'}), 400
        
        ip_fetched = get_device_ip(ip, user_id)
        if ip_fetched is not None:
            # print('ip repetido')
            return jsonify({'error_ip': 'IP en uso. Seleccione otro'}), 400

        # Insertar dispositivo en la base de datos
        insert_device(user_id, name, tag, type, mac=mac, ip=ip)
        return redirect(url_for('device.dashboard'))
    
    return render_template('add_device.html', name=name, mac=mac, ip=ip, role=user_role)

@device_bp.route('/remove_device', methods=['DELETE'])
def remove_device():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    name = request.args.get('name')
    tag = request.args.get('tag')
    if name is None or tag is None:
        return jsonify({'error': 'No se proporcionaron datos JSON'}), 400
    
    remove_device_by_tag(tag)
    return '', 204

@device_bp.route('/update_device_name', methods=['PUT'])
def update_device_name():
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    data = request.get_json()
    if data is None:
        return jsonify({'error': 'No se proporcionaron datos JSON'}), 400
    name = data.get('name')
    tag = data.get('tag')
    if name is None or tag is None:
        return jsonify({'error_tag_name': 'Name or Tag missing'}), 400
    # print(f"Name: {name}, Tag: {tag}")
    update_device_name_by_tag(tag, name)
    return jsonify({'success': True}), 200

