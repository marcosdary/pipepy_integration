from datetime import datetime

def validate_string_null(value: str) -> str:
    if value is None:
        raise ValueError("Campo obrigatório")
    if isinstance(value, str):
        value = value.strip()

        if value == "":
            raise ValueError("Campo não pode ser vazio")

        if value.lower() in {"null", "none", "undefined"}:
            raise ValueError("Campo inválido")
    return value

def validate_list(value: list) -> list:
    if len(value) == 0:
        raise ValueError("Não pode ser vazio")
    return value

def validate_datetime(value: str) -> list:
    try:
        return datetime.fromisoformat(value)
    except Exception as exc:
        raise ValueError("Formato inválido de data ISO.")
    
def validate_asset_value(value: int) -> int:
    if value > 0:
        return value
    raise ValueError("O valor de patrimônio inválido.")