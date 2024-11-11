import pytest

from unittest.mock import Mock
from main.models.AcceptanceCriteria import AcceptanceCriteria
from main.services.NLPService import Lists

@pytest.fixture
def list_service():
    return Lists(Mock(), Mock(), Mock())

@pytest.fixture
def ac():
    ac = AcceptanceCriteria("text", "text")
    ac.context = "text"
    ac.event = "text"
    ac.outcome = "text"
    ac.context_and_clauses = ["text"]
    ac.event_and_clauses = ["text"]
    ac.outcome_and_clauses = ["text"]
    return ac

# has lists tests
def test_has_no_lists_returns_false(list_service, ac):
    list_service.punctuation_service.remove_all_quotes_from_string = Mock(return_value=ac.original_lower_text)
    list_service.pos_service.extract_noun_phrases = Mock(return_value=[])
    list_service.get_potential_lists = Mock(return_value={})
    list_service.has_list = Mock(return_value=True)
    assert list_service.check_for_lists(ac.original_lower_text)

def test_has_lists_returns_true(list_service, ac):
    list_service.punctuation_service.remove_all_quotes_from_string = Mock(return_value=ac.original_lower_text)
    list_service.pos_service.extract_noun_phrases = Mock(return_value=[])
    list_service.get_potential_lists = Mock(return_value={})
    list_service.has_list = Mock(return_value=False)
    assert not list_service.check_for_lists(ac.original_lower_text)

# find potential lists tests
def test_get_potential_lists_basic(list_service):
    text = "apple, banana cherry, date"
    noun_phrases = ["apple", "banana", "cherry", "date"]
    expected_output = {0: ["apple", "banana", "cherry", "date"]}
    assert list_service.get_potential_lists(text, noun_phrases) == expected_output

def test_get_potential_lists_no_adjacent(list_service):
    text = "apple banana cherry date"
    noun_phrases = ["apple", "date"]
    expected_output = {}
    assert list_service.get_potential_lists(text, noun_phrases) == expected_output

def test_get_potential_lists_complex(list_service):
    text = "apple and banana cherry date, eggplant, fig grape"
    noun_phrases = ["apple", "banana", "date", "eggplant", "fig"]
    expected_output = {0: ["apple", "banana", "date", "eggplant", "fig"]}
    assert list_service.get_potential_lists(text, noun_phrases) == expected_output

def test_get_potential_lists_overlap(list_service):
    text = "apple, banana apple, cherry, banana, apple"
    noun_phrases = ["apple", "banana", "cherry"]
    expected_output = {0: ["apple", "banana", "cherry"]}
    assert list_service.get_potential_lists(text, noun_phrases) == expected_output

def test_get_potential_lists_edge_cases(list_service):
    text = "apple banana cherry"
    noun_phrases = ["apple", "banana", "cherry"]
    expected_output = {0: ["apple", "banana", "cherry"]}
    assert list_service.get_potential_lists(text, noun_phrases) == expected_output

# has lists tests
def test_has_list_basic(list_service): #
    text = "apple, banana and cherry"
    potential_lists = {0: ["apple", "banana", "cherry"]}
    list_service.list_indicators = [",", "and", "or"]
    assert list_service.has_list(text, potential_lists)

def test_has_list_no_indicators(list_service):
    text = "apple banana cherry"
    potential_lists = {0: ["apple", "banana", "cherry"]}
    list_service.list_indicators = [",", "and", "or"]
    assert not list_service.has_list(text, potential_lists)

def test_has_list_single_item(list_service):
    text = "apple banana cherry"
    potential_lists = {0: ["apple"]}
    list_service.list_indicators = [",", "and", "or"]
    assert not list_service.has_list(text, potential_lists)

def test_has_list_multiple_lists(list_service): #
    text = "apple, banana and cherry; date or fig"
    potential_lists = {0: ["apple", "banana", "cherry"], 1: ["date", "fig"]}
    list_service.list_indicators = [",", "and", "or"]
    assert list_service.has_list(text, potential_lists)

def test_has_list_edge_cases(list_service): #
    text = "apple , banana or cherry"
    potential_lists = {0: ["apple", "banana", "cherry"]}
    list_service.list_indicators = [",", "and", "or"]
    assert list_service.has_list(text, potential_lists)

def test_has_list_no_list_items(list_service):
    text = "apple banana cherry"
    potential_lists = {}
    list_service.list_indicators = [",", "and", "or"]
    assert not list_service.has_list(text, potential_lists)