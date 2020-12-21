import graphene
from apps.user.schema import UserQueries, UserMutations
from apps.userprofile.schema import UserProfileQuery, UserProfileMutations


class Query(UserQueries, UserProfileQuery):
    pass


class Mutation(UserMutations, UserProfileMutations):
    pass


schema = graphene.Schema(mutation=Mutation, query=Query, auto_camelcase=True)
