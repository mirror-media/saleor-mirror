import graphene
from apps.user.schema import UserQueries, UserMutations


class Query(UserQueries):
    pass


class Mutation(UserMutations):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query, auto_camelcase=True)
