import pytest

from unittest.mock import Mock

from main.models.UserStory import UserStory
from main.services.ambiguity.AmbiguityAnalyser import Quantifiers

@pytest.fixture
def quantifiers_analyser():
    return Quantifiers(Mock(), Mock(), Mock(), Mock())

@pytest.fixture
def obj():
    return UserStory("", "")

# contains escape clauses tests
def test_contains_quantifiers_found(quantifiers_analyser):
    quantifiers_analyser.word_list_service.get_quantifiers_list = Mock(return_value=['some', 'many', 'several'])
    text = "This feature has many advantages and some disadvantages."
    result = quantifiers_analyser.contains_quantifiers(text)
    assert result == ['some', 'many']

def test_contains_quantifiers_not_found(quantifiers_analyser):
    quantifiers_analyser.word_list_service.get_quantifiers_list = Mock(return_value=['some', 'many', 'several'])
    text = "This feature has specific advantages and clear disadvantages."
    result = quantifiers_analyser.contains_quantifiers(text)
    assert result == []

def test_contains_quantifiers_empty_text(quantifiers_analyser):
    quantifiers_analyser.word_list_service.get_quantifiers_list = Mock(return_value=['some', 'many', 'several'])
    text = ""
    result = quantifiers_analyser.contains_quantifiers(text)
    assert result == []

def test_contains_quantifiers_no_vague_terms_in_list(quantifiers_analyser):
    quantifiers_analyser.word_list_service.get_quantifiers_list = Mock(return_value=[])
    text = "This feature has many advantages and some disadvantages."
    result = quantifiers_analyser.contains_quantifiers(text)
    assert result == []

# is non-commital tests
def test_is_vague_with_escape_clauses(obj, quantifiers_analyser):
    quantifiers_analyser.contains_quantifiers = Mock(return_value=['some', 'many'])
    quantifiers_analyser.has_quantifiers(obj)
    assert quantifiers_analyser.ambiguity_types.ambiguity in obj.defects
    assert quantifiers_analyser.ambiguity_messages.quantifiers(['some', 'many']) in obj.defects[quantifiers_analyser.ambiguity_types.ambiguity]

def test_is_vague_without_escape_clauses(obj, quantifiers_analyser):
    quantifiers_analyser.contains_quantifiers = Mock(return_value=[])
    quantifiers_analyser.has_quantifiers(obj)
    assert quantifiers_analyser.ambiguity_types.ambiguity not in obj.defects