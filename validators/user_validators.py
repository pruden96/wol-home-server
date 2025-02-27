import re

from models import get_user_by_email, get_user_by_username


def validate_username(username: str) -> bool:
    """Valida que el username tenga solo caracteres alfanuméricos y sea de 4 a 20 caracteres."""
    return bool(re.fullmatch(r"^[a-zA-Z0-9_]{4,20}$", username))


def is_username_taken(username: str) -> bool:
    """Verifica si el username ya está registrado en la base de datos."""
    return get_user_by_username(username) is not None


def is_email_taken(email: str) -> bool:
    """Verifica si el email ya está registrado en la base de datos."""
    return get_user_by_email(email) is not None


def validate_email(email: str) -> bool:
    """Valida que el email tenga un formato válido."""
    return bool(
        re.fullmatch(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email)
    )
