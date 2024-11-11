import pytest

from unittest.mock import Mock
from main.services.NLPService import Brackets

@pytest.fixture
def bracket_service():
    return Brackets()

# remove references tests
def test_remove_references_basic(bracket_service):
    text = "This is a test sentence [1]."
    expected_output = "This is a test sentence ."
    assert bracket_service.remove_references(text) == expected_output

def test_remove_references_multiple(bracket_service):
    text = "This is a test sentence [1]. Here is another one [2]."
    expected_output = "This is a test sentence . Here is another one ."
    assert bracket_service.remove_references(text) == expected_output

def test_remove_references_no_references(bracket_service):
    text = "This is a test sentence."
    expected_output = "This is a test sentence."
    assert bracket_service.remove_references(text) == expected_output

def test_remove_references_edge_case(bracket_service):
    text = "[1]This is a test sentence.[2]"
    expected_output = "This is a test sentence."
    assert bracket_service.remove_references(text) == expected_output

def test_remove_references_complex(bracket_service):
    text = "This[1] is a test[2] sentence with multiple[3] references."
    expected_output = "This is a test sentence with multiple references."
    assert bracket_service.remove_references(text) == expected_output

def test_remove_references_large_numbers(bracket_service):
    text = "This is a test sentence [123]."
    expected_output = "This is a test sentence ."
    assert bracket_service.remove_references(text) == expected_output

def test_remove_references_embedded_numbers(bracket_service):
    text = "This sentence has numbers like 1234 and references [5]."
    expected_output = "This sentence has numbers like 1234 and references ."
    assert bracket_service.remove_references(text) == expected_output

# check well formed brackets containing text
@pytest.mark.parametrize("text", [
    "There are (well formed) brackets {containing} text",
    "These are {well formed} brackets containing text",
    "These are ([{well formed}]) brackets containing text",
    "{These} are well formed brackets containing text",
    "[These are well formed brackets containing text]"
])
def test_well_formed_brackets_containing_text_returns_true(text, bracket_service):
    assert bracket_service.has_brackets_containing_information(text)

@pytest.mark.parametrize("text", [
    "There are not (well formed brackets containing} text",
    "These are not {well formed brackets containing text",
    "These are not {well formed] brackets containing text]",
    "These} are not well formed brackets containing text",
    "These are not well formed brackets containing text]",
    "This has no brackets",
    "This has {} [] () brackets with no content"
])
def test_badly_formed_missing_text_returns_false(text, bracket_service):
    assert len(bracket_service.has_brackets_containing_information(text)) == 0