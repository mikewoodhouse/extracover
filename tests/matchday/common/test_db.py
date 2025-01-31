import pytest

from matchday.common.db import string_to_parameter


@pytest.mark.parametrize(
    "input,expected",
    [
        ("SELECT * FROM '{{some_table}}'", "SELECT * FROM :some_table"),
        ("SELECT * FROM '{{another_table}}' WHERE name='{{name}}'", "SELECT * FROM :another_table WHERE name=:name"),
    ],
)
def test_string_to_parameter(input: str, expected: str):
    assert string_to_parameter(input) == expected
