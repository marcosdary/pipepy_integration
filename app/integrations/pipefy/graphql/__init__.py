from strawberry.fastapi import GraphQLRouter
from strawberry.schema import Schema

from app.integrations.pipefy.graphql import query, mutation

schema = Schema(
    query=query.Query,
    mutation=mutation.Mutation
)

router = GraphQLRouter(schema=schema)
