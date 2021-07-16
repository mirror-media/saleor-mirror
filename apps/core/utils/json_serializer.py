from __future__ import division, unicode_literals
from django.core.serializers.json import DjangoJSONEncoder, Serializer as JsonSerializer
# from draftjs_sanitizer import SafeJSONEncoder
from decimal import Decimal
from typing import Union

from apps.core.utils.models import Money

MONEY_TYPE = "Money"
Numeric = Union[int, Decimal]


class Serializer(JsonSerializer):
    def _init_options(self):
        super()._init_options()
        self.json_kwargs["cls"] = CustomJsonEncoder


class CustomJsonEncoder(DjangoJSONEncoder):
    def default(self, obj):
        if isinstance(obj, Money):
            return {"_type": MONEY_TYPE, "amount": obj.amount, "currency": obj.currency}
        return super().default(obj)

# class HTMLSafeJSON(SafeJSONEncoder, DjangoJSONEncoder):
#     """Escape dangerous characters from JSON.
#
#     It is used for integrating JSON into HTML content in addition to
#     serializing Django objects.
#     """
