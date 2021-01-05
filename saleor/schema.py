import graphene
from apps.user.schema import UserQueries, UserMutations
from apps.user.schema import CoreMutations


class Query(UserQueries):
    pass


class Mutation(UserMutations, CoreMutations):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query, auto_camelcase=True)
