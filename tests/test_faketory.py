from pytest import raises

from .cases import BaseTestCase
from .factories import Factory, SampleFactory, SampleDjangoFactory


class _Factory:
    class TestCase(BaseTestCase):
        factory = Factory

        def test_quantity_below_1_returns_ERROR(self):
            number = self.fake.pyint(min_value=-100, max_value=0)
            with raises(ValueError):
                self.factory(_quantity=number)

        def test_quantity_below_1_returns_ERROR_even_if_list(self):
            number = self.fake.pyint(min_value=-100, max_value=0)
            with raises(ValueError):
                self.factory(_quantity=number, _list=True)


class TestFactory(_Factory.TestCase):
    def test_blank_init_returns_one_element(self):
        element = self.factory()
        assert isinstance(element.email, str)
        assert isinstance(element.name, str)

    def test_custom_values_override_default_ones_returns_one_element(self):
        email = self.fake.email()
        name = self.fake.name()
        element = self.factory(email=email, name=name)
        assert element.email == email
        assert element.name == name

    def test_quantity_blank_returns_one_element_if_list(self):
        element = self.factory(_list=True)
        assert isinstance(element.email, str)
        assert isinstance(element.name, str)

    def test_quantity_2_or_more_returns_many_elements(self):
        number_of_elements = self.fake.pyint(min_value=2, max_value=20)
        elements = self.factory(_quantity=number_of_elements)
        count = 0
        for element in elements:
            assert isinstance(element.email, str)
            assert isinstance(element.name, str)
            count += 1

        assert count == number_of_elements

    def test_quantity_2_or_more_returns_many_elements_as_a_list_if_list(self):
        number_of_elements = self.fake.pyint(min_value=2, max_value=20)
        elements = self.factory(_quantity=number_of_elements, _list=True)
        assert len(elements) == number_of_elements
        for element in elements:
            assert isinstance(element.email, str)
            assert isinstance(element.name, str)


class TestSampleFactory(TestFactory):
    factory = SampleFactory

    def test_blank_init_returns_one_element(self):
        element = self.factory()
        assert isinstance(element.age, int)
        assert isinstance(element.email, str)
        assert isinstance(element.name, str)


class TestSampleDjangoFactory(TestFactory):
    factory = SampleDjangoFactory

    def test_save_returns_triggers_resolver(self):
        element = self.factory(_resolver='save')
        assert isinstance(element.age, int)
        assert isinstance(element.email, str)
        assert isinstance(element.name, str)
        assert element.year == 3000
