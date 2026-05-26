from pydantic import ConfigDict, BaseModel
from app.core.constants import TypeOfRequest

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


def validate_asset_value(value: int) -> int:
    if value > 0:
        return value
    raise ValueError("O valor de patrimônio inválido.")

class CustomerBaseSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)


