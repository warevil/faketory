from faketory.factory import Faketory
from faketory.fake import Fake

from .models import Sample, SampleChild, SampleDjango


class Factory(Faketory):
    email = Fake('email')
    name = Fake('name')

    class Meta:
        model = Sample


class SampleFactory(Faketory):
    age = Fake('pyint', min_value=18)
    email = Fake('email')
    name = Fake('name')

    class Meta:
        model = SampleChild


class SampleDjangoFactory(Faketory):
    age = Fake('pyint', min_value=18)
    email = Fake('email')
    name = Fake('name')
    year = Fake('pyint', min_value=1900, max_value=2000)

    class Meta:
        model = SampleDjango
