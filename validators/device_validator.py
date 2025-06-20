import re


def validate_device_name(username: str) -> bool:
    """Valida que el nombre de dispositivo tenga solo caracteres alfanuméricos y sea de 3 a 15 caracteres."""
    return bool(re.fullmatch(r"^[a-zA-Z0-9 ]{3,15}$", username))


def validate_mac_address(mac: str) -> bool:
    """Valida si una dirección MAC tiene un formato correcto"""
    pattern = r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"
    return bool(re.fullmatch(pattern, mac))


def validate_device_tag(username: str) -> bool:
    """Valida que el TAG de dispositivo tenga solo caracteres alfanuméricos y sea de 2 a 8 caracteres."""
    return bool(re.fullmatch(r"^[a-zA-Z0-9]{2,8}$", username))
