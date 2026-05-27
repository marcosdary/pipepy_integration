# Mutation responsável pela criação de cards no Pipefy
#
# Variáveis esperadas:
#   - input:
#       Dados necessários para criação do card.
PIPEFY_CARD_MUTATION: str = """
mutation PipefyCardInput($input: PipefyCardInput!)
{
    createCard(input: $input) {
        card {
            title
        }
    }
}
"""


# Mutation responsável pela atualização
# de múltiplos campos de um card
#
# Variáveis esperadas:
#   - status:
#       Atualiza o campo de status do card.
#
#   - prioridade:
#       Atualiza o campo de prioridade do card.
UPDATE_CARD_FIELDS: str = """
mutation UpdateCardFields(
    $status: PipefyFieldUpdateInput!,
    $prioridade: PipefyFieldUpdateInput!
) {
    updateStatus: updateCardField(input: $status) {
        success
    }

    updatePrioridade: updateCardField(input: $prioridade) {
        success
    }
}
"""