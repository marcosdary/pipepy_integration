import strawberry
from strawberry.exceptions import StrawberryGraphQLError

@strawberry.type
class Query:
    
    @strawberry.field
    async def health(self) -> str:
        try:
            return "ok"
        except Exception as exc:
            raise StrawberryGraphQLError(str(exc))
    


