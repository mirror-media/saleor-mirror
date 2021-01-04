import graphene
from django.db import IntegrityError
from django.utils import timezone
from graphene_django.types import DjangoObjectType
from graphql_auth.settings import GraphQLAuthSettings, DEFAULTS
from graphql_jwt import ObtainJSONWebToken, Verify
from graphql_jwt.exceptions import JSONWebTokenError
from django.contrib.auth import get_user_model

from .models import CustomUser
from graphql_auth import mutations

# from .utils import md5
import hashlib
from django.db.models.functions import datetime

app_settings = GraphQLAuthSettings(None, DEFAULTS)

def md5(email):
    m = hashlib.md5()
    encoding = (email + str(datetime.datetime.now().timestamp())).encode('utf-8')
    m.update(encoding)
    hashed_email = m.hexdigest()
    return hashed_email


class MemberType(DjangoObjectType):
    class Meta:
        model = CustomUser
        name = 'member'
        fields = ('id', 'last_login', 'is_superuser', 'username', 'email', 'is_staff',
                  'is_active', 'date_joined', 'name', 'gender', 'phone', 'birthday',
                  'country', 'city', 'district', 'address', 'firebase_id', 'nickname')


class UserQueries(graphene.ObjectType):
    class Arguments:
        firebase_id = graphene.String(required=True)

    member = graphene.Field(MemberType, firebase_id=graphene.String(required=True))

    def resolve_member(self, info, firebase_id):
        return CustomUser.objects.get(firebase_id=firebase_id)


class CreateMember(graphene.Mutation):
    class Arguments:
        email = graphene.String(required=True)
        firebase_id = graphene.String(required=True)
        nickname = graphene.String()

    member = graphene.Field(MemberType)
    success = graphene.Boolean()
    msg = graphene.String()

    @classmethod
    def mutate(cls, root, info, email, firebase_id, **kwargs):
        member = CustomUser(email=email, firebase_id=firebase_id)

        if kwargs.get('nickname'):
            nickname = kwargs.get('nickname')

        success = True
        try:
            member.save()
            return CreateMember(member=member, success=success,
                                msg="You have been registered.")

        except IntegrityError as dberror:
            if 'duplicate key value violates unique constraint' in dberror.args[0]:
                return CreateMember(member=None, success=True,
                                    msg="This email or firebaseId has already exist.")
            else:
                raise dberror


class DeleteMember(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        firebase_id = graphene.String(required=True)

    @classmethod
    def mutate(cls, root, info, firebase_id):
        member_instance = CustomUser.objects.get(firebase_id=firebase_id)
        if member_instance:
            member_instance.email = md5(member_instance.email)
            member_instance.name = None
            member_instance.phone = None
            member_instance.country = None
            member_instance.city = None
            member_instance.district = None
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

        country = graphene.String()
        city = graphene.String()
        district = graphene.String()

        address = graphene.String()
        profile_image = graphene.String()

    class Meta:
        exclude = ["password"]

    member = graphene.Field(MemberType)
    success = graphene.Boolean()

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


class Error(graphene.ObjectType):
    field = graphene.String(
        description=(
            "Name of a field that caused the error. A value of `null` indicates that "
            "the error isn't associated with a particular field."
        ),
        required=False,
    )
    message = graphene.String(description="The error message.")

    class Meta:
        description = "Represents an error in the input of a mutation."


class CreateToken(ObtainJSONWebToken):
    member = graphene.Field(MemberType, description="Member Instance")
    errors = graphene.List(
        graphene.NonNull(Error),
        required=True)

    @classmethod
    def mutate(cls, root, info, **kwargs):
        try:
            result = super().mutate(root, info, **kwargs)
        except JSONWebTokenError as e:
            errors = [Error(message=str(e))]
            # account_errors = []
            return CreateToken(errors=errors)
        # except ValidationError as e:
        #     errors = validation_error_to_error_type(e)
        #     return cls.handle_typed_errors(errors)
        else:
            member = result.member
            member.last_login = timezone.now()
            member.save(update_fields=["last_login"])
            return result

    @classmethod
    def resolve(cls, root, info, **kwargs):
        return cls(user=info.context.user, errors=[], account_errors=[])

class CoreMutations(graphene.ObjectType):
    token_create = mutations.ObtainJSONWebToken.Field()
    token_refresh = mutations.RefreshToken.Field()
    token_verify = mutations.VerifyToken.Field()
