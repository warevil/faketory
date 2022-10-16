from faketory.factory import Faketory
from faketory.gens import Fake, FaketoryGen

from .models import Sample, SampleChild, SampleDjango, SampleHasChild


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
    year = Fake('pyint', min_value=2000, max_value=2030)

    class Meta:
        model = SampleDjango


class SampleHasChildFactory(Faketory):
    child = FaketoryGen(SampleFactory)
    email = Fake('email')

    class Meta:
        model = SampleHasChild
