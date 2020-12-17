import graphene
from graphene_django.types import DjangoObjectType
from graphql_auth.bases import MutationMixin, DynamicArgsMixin
from graphql_auth.mixins import DeleteAccountMixin, ArchiveOrDeleteMixin
from graphql_auth.schema import UserQuery, MeQuery
from graphql_auth.settings import GraphQLAuthSettings, DEFAULTS
from graphql_auth.utils import revoke_user_refresh_token


from .models import CustomUser
from graphql_auth import mutations

app_settings = GraphQLAuthSettings(None, DEFAULTS)


class UserType(DjangoObjectType):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'last_login', 'date_joined')


class UserQueries(UserQuery, MeQuery,graphene.ObjectType):
    pass


class DeleteUpdate(ArchiveOrDeleteMixin):
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


class DeleteUpdate(MutationMixin, DeleteUpdate, DynamicArgsMixin, graphene.Mutation):
    __doc__ = DeleteUpdate.__doc__
    _required_args = ["id"]


class UserMutations(graphene.ObjectType):
    register = mutations.Register.Field()
    verify_account = mutations.VerifyAccount.Field()
    resend_activation_email = mutations.ResendActivationEmail.Field()
    send_password_reset_email = mutations.SendPasswordResetEmail.Field()
    password_reset = mutations.PasswordReset.Field()
    password_set = mutations.PasswordSet.Field()
    password_change = mutations.PasswordChange.Field()
    archive_account = mutations.ArchiveAccount.Field()
    delete_account = DeleteUpdate.Field()
    update_account = mutations.UpdateAccount.Field()
    send_secondary_email_activation = mutations.SendSecondaryEmailActivation.Field()
    verify_secondary_email = mutations.VerifySecondaryEmail.Field()
    swap_emails = mutations.SwapEmails.Field()

    # django-graphql-jwt authentication
    # with some extra features
    token_auth = mutations.ObtainJSONWebToken.Field()
    verify_token = mutations.VerifyToken.Field()
    refresh_token = mutations.RefreshToken.Field()
    revoke_token = mutations.RevokeToken.Field()
