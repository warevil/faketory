# Copyright (c) 2022 warevil <jg@warevil.dev>

import operator
from inspect import getmembers
from itertools import repeat

from .gens import Fake, FaketoryGen
from .placeholders.models import SomeModel


def build(__Model, __resolver=None, **fields):
    '''Builds a fake model instance.'''
    model_fields = {
        field_name: value.generate()
        if isinstance(value, Fake) or isinstance(value, FaketoryGen)
        else value
        for field_name, value in fields.items()
    }
    model_instance = __Model(**model_fields)
    if __resolver:
        resolver = operator.attrgetter(__resolver)(model_instance)
        resolver()
    return model_instance


class Faketory:
    def __new__(cls, _qty: int = 1, _resolver=None, _type: str = 'list', **custom_fields):
        '''
        Returns 1 or more fake model instances of a Model class.
        _qty: Number of fake model instances to return. Minimum value is 1.
        _resolver: Function to resolve once the model instance is created.
        _type: Define the type of the model instance you want to return. Default: 'list'.
        **custom_fields: These fields will override the Fake generated values of the Factory.
        '''
        if _qty < 1:
            raise ValueError('Quantity must be greater than 0')

        instance = super().__new__(cls)
        fields = {
            attribute: getattr(instance, attribute)
            for attribute, var_type in getmembers(type(instance))
            if not attribute.startswith(('__', 'Meta'))
            # IMPORTANT: This is very likely to require an update
            and not str(var_type).startswith(('<bound method', '<function '))
        }
        fields.update(custom_fields)

        objects = (build(cls.Meta.model, _resolver, **fields) for _ in repeat(None, _qty))
        if _qty == 1:
            return next(objects)
        if _type == 'generator':  # NOTE: Will not produce any objects until consumed
            return objects
        if _type == 'set':
            return set(objects)
        # list is the default format
        return list(objects)

    class Meta:
        model = SomeModel
