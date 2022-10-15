from pytest import raises

from .cases import BaseTestCase
from .factories import Factory, SampleDjangoFactory, SampleFactory


class _Factory:
    class TestCase(BaseTestCase):
        factory = Factory

        def test_quantity_below_1_returns_ERROR(self):
            number = self.fake.pyint(min_value=-100, max_value=0)
            with raises(ValueError):
                self.factory(_qty=number)

        def test_quantity_below_1_returns_ERROR_even_if_list(self):
            number = self.fake.pyint(min_value=-100, max_value=0)
            with raises(ValueError):
                self.factory(_qty=number, _list=True)


class TestFactory(_Factory.TestCase):
    def _assert_fields(self, element):
        assert isinstance(element.email, str)
        assert isinstance(element.name, str)

    def test_blank_init_returns_one_element(self):
        element = self.factory()
        self._assert_fields(element)

    def test_custom_values_override_default_ones_returns_one_element(self):
        email = self.fake.email()
        name = self.fake.name()
        element = self.factory(email=email, name=name)
        assert element.email == email
        assert element.name == name

    def test_quantity_blank_returns_one_element_if_generator(self):
        element = self.factory(_type='generator')
        self._assert_fields(element)

    def test_quantity_blank_returns_one_element_if_list(self):
        element = self.factory(_type='list')
        self._assert_fields(element)

    def test_quantity_blank_returns_one_element_if_set(self):
        element = self.factory(_type='set')
        self._assert_fields(element)

    def test_quantity_2_or_more_returns_many_elements_as_list_by_default(self):
        quantity = self.fake.pyint(min_value=2, max_value=20)
        elements = self.factory(_qty=quantity, _type='list')
        assert len(elements) == quantity
        for element in elements:
            self._assert_fields(element)

    def test_quantity_2_or_more_returns_many_elements_if_generator_when_consumed(self):
        quantity = self.fake.pyint(min_value=2, max_value=20)
        elements = self.factory(_qty=quantity, _type='generator')
        element = next(elements)  # 1st element to verify it is a generator
        count = 1
        for element in elements:
            self._assert_fields(element)
            count += 1

        assert count == quantity

    def test_quantity_2_or_more_returns_many_elements_as_a_list_if_list(self):
        quantity = self.fake.pyint(min_value=2, max_value=20)
        elements = self.factory(_qty=quantity, _type='list')
        assert len(elements) == quantity
        for element in elements:
            self._assert_fields(element)

    def test_quantity_2_or_more_returns_many_elements_as_a_set_if_set(self):
        quantity = self.fake.pyint(min_value=2, max_value=20)
        elements = self.factory(_qty=quantity, _type='set')
        assert len(elements) == quantity
        for element in elements:
            self._assert_fields(element)


class TestSampleFactory(TestFactory):
    factory = SampleFactory

    def test_blank_init_returns_one_element(self):
        element = self.factory()
        assert isinstance(element.age, int)
        assert isinstance(element.email, str)
        assert isinstance(element.name, str)


class TestSampleDjangoFactory(TestFactory):
    factory = SampleDjangoFactory

    def _assert_sample_django_fields(self, element):
        assert isinstance(element.age, int)
        assert isinstance(element.email, str)
        assert isinstance(element.name, str)
        assert element.year == 3000

    def test_save_one_triggers_resolver(self):
        element = self.factory(_resolver='save')
        self._assert_sample_django_fields(element)

    def test_save_one_triggers_resolver_if_generator(self):
        element = self.factory(_resolver='save', _type='generator')
        self._assert_sample_django_fields(element)

    def test_save_one_triggers_resolver_if_set(self):
        element = self.factory(_resolver='save', _type='set')
        self._assert_sample_django_fields(element)

    def test_save_many_triggers_resolver(self):
        quantity = self.fake.pyint(min_value=2, max_value=20)
        elements = self.factory(_qty=quantity, _resolver='save')
        for element in elements:
            self._assert_sample_django_fields(element)

    def test_save_many_triggers_resolver_if_generator(self):
        quantity = self.fake.pyint(min_value=2, max_value=20)
        elements = self.factory(_qty=quantity, _resolver='save', _type='generator')
        for element in elements:
            self._assert_sample_django_fields(element)

    def test_save_many_triggers_resolver_if_set(self):
        quantity = self.fake.pyint(min_value=2, max_value=20)
        elements = self.factory(_qty=quantity, _resolver='save', _type='set')
        for element in elements:
            self._assert_sample_django_fields(element)
