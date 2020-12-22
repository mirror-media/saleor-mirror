import graphene
from graphene_django.types import DjangoObjectType
from graphql_auth.bases import MutationMixin, DynamicArgsMixin
from graphql_auth.mixins import DeleteAccountMixin, ArchiveOrDeleteMixin, RegisterMixin, \
    UpdateAccountMixin
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth.settings import GraphQLAuthSettings, DEFAULTS
from graphql_auth.utils import revoke_user_refresh_token, normalize_fields

from .models import CustomUser
from graphql_auth import mutations


app_settings = GraphQLAuthSettings(None, DEFAULTS)


class MemberType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = '__all__'


class UserQueries(UserQuery, MeQuery, graphene.ObjectType):
    pass


class _DeleteUpdate(ArchiveOrDeleteMixin):

    @classmethod
    def resolve_action(cls, user, *args, **kwargs):
        if app_settings.ALLOW_DELETE_ACCOUNT:
            revoke_user_refresh_token(user=user)
            # user.delete()
            user.anonymize()
        else:
            user.is_active = False
            user.save(update_fields=["is_active"])
            revoke_user_refresh_token(user=user)


# class DeleteUpdate(MutationMixin, _DeleteUpdate, DynamicArgsMixin, graphene.Mutation):
#     __doc__ = _DeleteUpdate.__doc__
#     _required_args = ["firebase_id"]

# class DeleteUpdate(graphene.Mutation):
#     class Arguments:
#         firebase_id = graphene.String(required=True)
#
#     def mutate(self):


class Register(MutationMixin, DynamicArgsMixin, RegisterMixin, graphene.Mutation):
    __doc__ = RegisterMixin.__doc__

    _required_args = ['email']
    _args = ['firebase_id', 'nickname']


class CreateMember(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        firebase_id = graphene.String(required=True)
        nickname = graphene.String()

    member = graphene.Field(MemberType)
    success = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, email, firebase_id, **kwargs):
        member = CustomUser(email=email, firebase_id=firebase_id)

        if kwargs.get('nickname'):
            nickname = kwargs.get('nickname')

        success = True
        member.save()

        return CreateMember(member=member, success=True)


class MemberInput(graphene.InputObjectType):
    nickname = graphene.String()
    name = graphene.String()
    gender = graphene.Int()
    phone = graphene.String()
    birthday = graphene.Date()
    address = graphene.String()
    profile_image = graphene.String()


class DeleteMember(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        firebase_id = graphene.String()

    @classmethod
    def mutate(cls, root, info, firebase_id):
        member_instance = CustomUser.objects.get(firebase_id=firebase_id)
        if member_instance:
            member_instance.firebase_id = None
            member_instance.name = None
            member_instance.phone = None
            member_instance.address = None
            member_instance.profile_image = None
            member_instance.is_active = False
            member_instance.nickname = None
            member_instance.save()

            return cls(success=True)
        else:
            return cls(success=False)


class UpdateMember(graphene.Mutation):
    class Arguments:
        firebase_id = graphene.String(required=True)
        nickname = graphene.String()
        name = graphene.String()
        gender = graphene.Int()
        phone = graphene.String()
        birthday = graphene.Date()
        address = graphene.String()
        profile_image = graphene.String()

    class Meta:
        exclude = ["password"]

    member = graphene.Field(MemberType)
    success = graphene.Boolean()

    # @login_required
    @staticmethod
    def mutate(root, info, firebase_id, **kwargs):
        success = False
        member_instance = CustomUser.objects.get(firebase_id=firebase_id)

        if member_instance:
            print(member_instance)
            success = True
            for k, v in kwargs.items():
                setattr(member_instance, k, v)
            member_instance.save()

            return UpdateMember(member=member_instance, success=success)
        else:
            print("SSSS")
            return UpdateMember(member=None, success=success)


class UserMutations(graphene.ObjectType):
    member = graphene.Field(MemberType)

    create_member = CreateMember.Field()
    update_member = UpdateMember.Field()
    delete_member = DeleteMember.Field()
    verify_member = mutations.VerifyAccount.Field()

    # resend_activation_email = mutations.ResendActivationEmail.Field()
    # send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    # password_reset = mutations.PasswordReset.Field()
    # password_set = mutations.PasswordSet.Field()
    # password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()

    # django-graphql-jwt authentication
    # with some extra features
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()
