import pytest

from tests.tests_meta.utils import (
    get_classes_from_script,
    get_sequence_class_names_from_markdown,
    get_sequences_defined_in_script,
)


@pytest.mark.parametrize(
    'script_path, pattern',
    [('sequence/sequences/integer/explicit.py', r'^A\d{6}$'),
     ('sequence/sequences/integer/explicit_generalised_sequences.py', None),
     ('sequence/sequences/integer/finite.py', r'^A\d{6}$'),
     ('sequence/sequences/integer/periodic.py', r'^A\d{6}$'),
     ('tests/tests_integer_sequences/test_periodic.py', None),
     ('sequence/sequences/integer/property_defined.py', r'^A\d{6}$'),
     ('sequence/sequences/integer/property_defined_generalised_sequences.py', None),
     ('sequence/sequences/integer/recursive.py', r'^A\d{6}$'),
     ('sequence/sequences/integer/recursive_generalised_sequences.py', None),
     ('tests/tests_integer_sequences/test_explicit.py', None),
     ('tests/tests_integer_sequences/test_finite.py', None),
     ('tests/tests_integer_sequences/test_periodic.py', None),
     ('tests/tests_integer_sequences/test_recursive.py', None)]
)
def test_order_script(script_path, pattern):
    """ The test checks if the script give at script_path is sorted alphabetically after filtered by pattern. """
    sequence_names = get_classes_from_script(script_path=script_path, pattern=pattern)
    assert sequence_names == sorted(sequence_names), f"Classes in '{script_path}' are not in alphabetical order."


@pytest.mark.parametrize(
    'script_path, pattern, test_script_path',
    [('sequence/sequences/integer/explicit.py', r'^A\d{6}$', 'tests/tests_integer_sequences/test_explicit.py'),
     ('sequence/sequences/integer/finite.py', r'^A\d{6}$', 'tests/tests_integer_sequences/test_finite.py'),
     ('sequence/sequences/integer/periodic.py', r'^A\d{6}$', 'tests/tests_integer_sequences/test_periodic.py'),
     ('sequence/sequences/integer/recursive.py', r'^A\d{6}$', 'tests/tests_integer_sequences/test_recursive.py')]
)
def test_every_sequence_is_tested(script_path, pattern, test_script_path):
    """ The test checks if for every sequence defined there is a test. """
    sequence_names = get_classes_from_script(script_path=script_path, pattern=pattern)
    test_names = get_classes_from_script(script_path=test_script_path)
    sequences_tested = [test.replace('Test', '') for test in test_names]

    sequences_not_tested = set(sequence_names).difference(set(sequences_tested))
    if sequences_not_tested:
        raise Exception(f'There are no tests for the following sequence/s: {sequences_not_tested}')


def test_markdown():
    """ The test checks if every defined sequence is also reported in the SEQUENCE_LIST.md, and vice-versa."""
    sequence_markdown = get_sequence_class_names_from_markdown()

    sequence_script_paths = [
        'sequence/sequences/integer/explicit.py',
        'sequence/sequences/integer/recursive.py',
        'sequence/sequences/integer/finite.py',
        'sequence/sequences/integer/periodic.py',
    ]
    sequence_scripts = set().union(
        *[get_sequences_defined_in_script(script_path) for script_path in sequence_script_paths]
    )

    sequences_in_markdown_but_not_in_scripts = sequence_markdown.difference(sequence_scripts)
    if sequences_in_markdown_but_not_in_scripts != set():
        raise ValueError(
            f"The following sequences are in the SEQUENCE_LIST.md,"
            f" but are not implemented: {', '.join(list(sequences_in_markdown_but_not_in_scripts))}"
        )
    sequences_in_scripts_but_not_in_markdown = sequence_scripts.difference(sequence_markdown)
    if sequences_in_scripts_but_not_in_markdown != set():
        raise ValueError(
            f"The following sequences are implemented,"
            f" but are not in SEQUENCE_LIST.md: {', '.join(list(sequences_in_scripts_but_not_in_markdown))}"
        )