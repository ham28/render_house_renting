import graphene
from property_managment.schema import Query as PropertyQuery

from property_managment.schema import Mutation as PropertyMutation
from user_managment.schema import Mutation as UserMutation


class Query(PropertyQuery, graphene.ObjectType):
    pass


class Mutation(PropertyMutation, UserMutation, graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query, mutation=Mutation)
