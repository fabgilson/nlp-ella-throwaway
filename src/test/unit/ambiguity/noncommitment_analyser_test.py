import pytest

from unittest.mock import Mock

from main.models.UserStory import UserStory
from main.services.ambiguity.AmbiguityAnalyser import NonCommitment

@pytest.fixture
def noncommitment_analyser():
    return NonCommitment(Mock(), Mock(), Mock(), Mock())

@pytest.fixture
def obj():
    return UserStory("", "")

# contains escape clauses tests
def test_contains_escape_clauses_found(noncommitment_analyser):
    noncommitment_analyser.word_list_service.get_escape_clause_list = Mock(return_value=['some', 'many', 'several'])
    text = "This feature has many advantages and some disadvantages."
    result = noncommitment_analyser.contains_escape_clauses(text)
    assert result == ['some', 'many']

def test_contains_escape_clauses_not_found(noncommitment_analyser):
    noncommitment_analyser.word_list_service.get_escape_clause_list = Mock(return_value=['some', 'many', 'several'])
    text = "This feature has specific advantages and clear disadvantages."
    result = noncommitment_analyser.contains_escape_clauses(text)
    assert result == []

def test_contains_escape_clauses_empty_text(noncommitment_analyser):
    noncommitment_analyser.word_list_service.get_escape_clause_list = Mock(return_value=['some', 'many', 'several'])
    text = ""
    result = noncommitment_analyser.contains_escape_clauses(text)
    assert result == []

def test_contains_escape_clauses_no_vague_terms_in_list(noncommitment_analyser):
    noncommitment_analyser.word_list_service.get_escape_clause_list = Mock(return_value=[])
    text = "This feature has many advantages and some disadvantages."
    result = noncommitment_analyser.contains_escape_clauses(text)
    assert result == []

# is non-commital tests
def test_is_vague_with_escape_clauses(obj, noncommitment_analyser):
    noncommitment_analyser.contains_escape_clauses = Mock(return_value=['some', 'many'])
    noncommitment_analyser.is_non_commital(obj)
    assert noncommitment_analyser.ambiguity_types.ambiguity in obj.defects
    assert noncommitment_analyser.ambiguity_messages.escape_clauses(['some', 'many']) in obj.defects[noncommitment_analyser.ambiguity_types.ambiguity]

def test_is_vague_without_escape_clauses(obj, noncommitment_analyser):
    noncommitment_analyser.contains_escape_clauses = Mock(return_value=[])
    noncommitment_analyser.is_non_commital(obj)
    assert noncommitment_analyser.ambiguity_types.ambiguity not in obj.defects