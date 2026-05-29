from datetime import datetime


def validate_string_null(value: str) -> str:
    """
    Valida campos de texto obrigatórios.

    A validação verifica:
        - Se o valor é nulo.
        - Se o valor está vazio.
        - Se contém valores inválidos como:
          "null", "none" ou "undefined".

    Args:
        value:
            Valor textual a ser validado.

    Returns:
        str:
            Valor validado e tratado.

    Raises:
        ValueError:
            Caso o valor seja inválido.
    """

    # Verifica se o valor é nulo
    if value is None:
        raise ValueError(
            "Campo obrigatório"
        )

    # Remove espaços em branco
    if isinstance(value, str):
        value = value.strip()

        # Verifica se o campo está vazio
        if value == "":
            raise ValueError(
                "Campo não pode ser vazio"
            )

        # Valida palavras reservadas inválidas
        if value.lower() in {
            "null",
            "none",
            "undefined"
        }:
            raise ValueError(
                "Campo inválido"
            )

    return value


def validate_list(value: list) -> list:
    """
    Valida listas obrigatórias.

    Args:
        value:
            Lista a ser validada.

    Returns:
        list:
            Lista validada.

    Raises:
        ValueError:
            Caso a lista esteja vazia.
    """

    # Verifica se a lista possui elementos
    if len(value) == 0:
        raise ValueError(
            "Não pode ser vazio"
        )

    return value


def validate_datetime(value: str) -> datetime:
    """
    Valida datas no formato ISO.

    Args:
        value:
            Data em formato string ISO.

    Returns:
        datetime:
            Objeto datetime convertido.

    Raises:
        ValueError:
            Caso a data possua formato inválido.
    """

    try:
        # Converte a string para datetime
        return datetime.fromisoformat(value)

    except Exception:
        raise ValueError(
            "Formato inválido de data ISO."
        )


def validate_asset_value(value) -> int:
    """
    Valida o valor patrimonial informado.

    O valor deve ser maior que zero.

    Args:
        value:
            Valor patrimonial.

    Returns:
        int:
            Valor validado.

    Raises:
        ValueError:
            Caso o valor seja inválido.
    """

    # Verifica se o patrimônio é válido
    if not isinstance(value, int):
        raise ValueError("O valor deve ser inteiro")
    

    if value > 0:
        return value

    raise ValueError(
        "O valor de patrimônio inválido."
    )