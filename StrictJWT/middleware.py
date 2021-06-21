from graphql_jwt.exceptions import JSONWebTokenError
from graphql_jwt.middleware import JSONWebTokenMiddleware
from django.contrib.auth import authenticate
from django.contrib.auth.middleware import get_user
from django.contrib.auth.models import AnonymousUser
from django.utils.translation import gettext as _
from graphql_jwt.settings import jwt_settings
from graphql_jwt.utils import get_token_argument


def _authenticate(request):
    is_anonymous = not hasattr(request, 'user') or request.user.is_anonymous
    return is_anonymous and get_http_authorization(request) is not None


def get_http_authorization(request):
    auth = request.META.get(jwt_settings.JWT_AUTH_HEADER_NAME, '').split()
    prefix = jwt_settings.JWT_AUTH_HEADER_PREFIX

    if len(auth) != 2:
        raise JSONWebTokenError(_(f'Invalid HTTP Authorization header'))

    if auth[0].lower() != prefix.lower():
        print("FALSE TOKEN")
        raise JSONWebTokenError(_(f'Incorrect HTTP Authorization header prefix: {auth[0]}'))
    return auth[1]


class StrictMiddleware(JSONWebTokenMiddleware):
    ALLOWED_MUTATIONS = [
        # "checkoutAddPromoCode",
        # "checkoutBillingAddressUpdate",
        # "checkoutComplete",
        # "checkoutCreate",
        # "checkoutCustomerAttach",
        # "checkoutCustomerDetach",
        # "checkoutEmailUpdate",
        # "checkoutLineDelete",
        # "checkoutLinesAdd",
        # "checkoutLinesUpdate",
        # "checkoutRemovePromoCode",
        # "checkoutPaymentCreate",
        # "checkoutShippingAddressUpdate",
        # "checkoutShippingMethodUpdate",
        "tokenCreate",
        "tokenVerify",
    ]

    def resolve(self, next, root, info, **kwargs):
        operation = info.operation.operation
        if operation != "mutation":
            return next(root, info, **kwargs)

        context = info.context
        token_argument = get_token_argument(context, **kwargs)

        if jwt_settings.JWT_ALLOW_ARGUMENT and token_argument is None:
            user = self.cached_authentication.parent(info.path)

            if user is not None:
                context.user = user

            elif hasattr(context, 'user'):
                if hasattr(context, 'session'):
                    context.user = get_user(context)
                    self.cached_authentication.insert(info.path, context.user)
                else:
                    context.user = AnonymousUser()

        if ((_authenticate(context) or token_argument is not None) and
                self.authenticate_context(info, **kwargs)):

            user = authenticate(request=context, **kwargs)

            if user is not None:
                context.user = user

                if jwt_settings.JWT_ALLOW_ARGUMENT:
                    self.cached_authentication.insert(info.path, user)
        for selection in info.operation.selection_set.selections:
            selection_name = str(selection.name.value)
            blocked = selection_name not in self.ALLOWED_MUTATIONS
            if blocked:
                raise Exception(
                    "Be aware admin pirate! API runs in read-only mode!"
                )

        return next(root, info, **kwargs)
