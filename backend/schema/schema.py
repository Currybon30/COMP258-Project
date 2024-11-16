from graphene import Schema
from schema.queries import Query
from schema.mutations import Mutation

schema = Schema(query=Query, mutation=Mutation)
