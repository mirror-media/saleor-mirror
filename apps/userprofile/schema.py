import graphene
from graphene_django.types import DjangoObjectType
from .models import Profile


class ProfileType(DjangoObjectType):
    class Meta:
        model = Profile
        fields = ('user', 'bio', 'phone_number')


class UserProfileQuery(graphene.ObjectType):
    all_profile = graphene.List(ProfileType)

    def resolve_all_profiles(self, info, **kwargs):
        return Profile.objects.all()


class UserProfileMutations(graphene.Mutation):
    class Arguments:
        birthday = graphene.Date()

        bio = graphene.String(required=True)
        id = graphene.ID()

    profile = graphene.Field(ProfileType)

    @staticmethod
    def mutate(self):
        pass

