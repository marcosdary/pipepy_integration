
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

UPDATE_CARD_FIELDS: str = """
mutation UpdateCardFields(
    $status: PipefyFieldUpdateInput!, 
    $prioridade: PipefyFieldUpdateInput!
) {
    updateStatus: updateCardField(input: $status){
        success
    }

    updatePrioridade: updateCardField(input: $prioridade){
        success
    }
}
""" 