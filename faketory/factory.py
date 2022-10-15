# Copyright (c) 2022 warevil <jg@warevil.dev>

import operator
from itertools import repeat

from .fake import Fake
from .placeholders.models import SomeModel


def build_object(__Model, __resolver=None, **fields):
    model_fields = {
        field_name: value.generate() if isinstance(value, Fake) else value
        for field_name, value in fields.items()
    }
    model_instance = __Model(**model_fields)
    if __resolver:
        resolver = operator.attrgetter(__resolver)(model_instance)
        resolver()
    return model_instance


class Faketory:
    def __new__(
        cls,
        _quantity: int = 1,
        _resolver=None,
        _type: str = 'list',
        **custom_fields,
    ):
        if _quantity < 1:
            raise ValueError('Quantity must be greater than 0')

        instance = super().__new__(cls)
        fields = {
            attribute: getattr(instance, attribute)
            for attribute, var_type in type(instance).__dict__.items()
            if not attribute.startswith(('__', 'Meta'))
            # IMPORTANT: This is very likely to require an update
            and not str(var_type).startswith(('<bound method', '<function '))
        }
        fields.update(custom_fields)

        objects = (
            build_object(cls.Meta.model, _resolver, **fields) for _ in repeat(None, _quantity)
        )
        if _quantity == 1:
            return next(objects)
        if _type == 'generator':  # NOTE: Will not produce any objects until consumed
            return objects
        if _type == 'set':
            return set(objects)
        # list is the default format
        return list(objects)

    class Meta:
        model = SomeModel
