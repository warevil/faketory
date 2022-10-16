from itertools import repeat

from faketory.gens import Fake


def test_unique_values():
    expected_quantity = 50
    numbers = {
        Fake('unique.random_int', min=1, max=expected_quantity).generate()
        for _ in repeat(None, expected_quantity)
    }
    assert len(numbers) == expected_quantity
    for number in numbers:
        assert number < expected_quantity + 1
