from datetime import datetime

from app.exceptions import UnprocessableEntity

def validate_string_null(value: str) -> str:
    if value is None:
        raise UnprocessableEntity("Campo obrigatório")
    if isinstance(value, str):
        value = value.strip()

        if value == "":
            raise UnprocessableEntity("Campo não pode ser vazio")

        if value.lower() in {"null", "none", "undefined"}:
            raise UnprocessableEntity("Campo inválido")
    return value

def validate_list(value: list) -> list:
    if len(value) == 0:
        raise UnprocessableEntity("Não pode ser vazio")
    return value

def validate_datetime(value: str) -> list:
    try:
        return datetime.fromisoformat(value)
    except Exception as exc:
        raise UnprocessableEntity("Formato inválido de data ISO.")
    
def validate_asset_value(value: int) -> int:
    if value > 0:
        return value
    raise UnprocessableEntity("O valor de patrimônio inválido.")