import operator

from faker import Faker

_fake = Faker()


class Fake:
    def __init__(self, __method_name, **fields):
        self.method = operator.attrgetter(__method_name)(_fake)
        self.fields = fields

    def generate(self):
        return self.method(**self.fields)
