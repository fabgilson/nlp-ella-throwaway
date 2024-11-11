import pytest

from unittest.mock import Mock

from main.models.UserStory import UserStory
from main.services.ambiguity.AmbiguityAnalyser import Vagueness

@pytest.fixture
def vagueness_analyser():
    return Vagueness(Mock(), Mock(), Mock(), Mock())

@pytest.fixture
def obj():
    return UserStory("", "")

# contains vague terms tests
def test_contains_vague_terms_found(vagueness_analyser):
    vagueness_analyser.word_list_service.get_vague_terms_list = Mock(return_value=['some', 'many', 'several'])
    text = "This feature has many advantages and some disadvantages."
    result = vagueness_analyser.contains_vague_terms(text)
    assert result == ['some', 'many']

def test_contains_vague_terms_not_found(vagueness_analyser):
    vagueness_analyser.word_list_service.get_vague_terms_list = Mock(return_value=['some', 'many', 'several'])
    text = "This feature has specific advantages and clear disadvantages."
    result = vagueness_analyser.contains_vague_terms(text)
    assert result == []

def test_contains_vague_terms_empty_text(vagueness_analyser):
    vagueness_analyser.word_list_service.get_vague_terms_list = Mock(return_value=['some', 'many', 'several'])
    text = ""
    result = vagueness_analyser.contains_vague_terms(text)
    assert result == []

def test_contains_vague_terms_no_vague_terms_in_list(vagueness_analyser):
    vagueness_analyser.word_list_service.get_vague_terms_list = Mock(return_value=[])
    text = "This feature has many advantages and some disadvantages."
    result = vagueness_analyser.contains_vague_terms(text)
    assert result == []

# is vague tests
def test_is_vague_with_vague_terms(obj, vagueness_analyser):
    vagueness_analyser.contains_vague_terms = Mock(return_value=['some', 'many'])
    vagueness_analyser.is_vague(obj)
    assert vagueness_analyser.ambiguity_types.ambiguity in obj.defects
    assert vagueness_analyser.ambiguity_messages.vague_terms(['some', 'many']) in obj.defects[vagueness_analyser.ambiguity_types.ambiguity]

def test_is_vague_without_vague_terms(obj, vagueness_analyser):
    vagueness_analyser.contains_vague_terms = Mock(return_value=[])
    vagueness_analyser.is_vague(obj)
    assert vagueness_analyser.ambiguity_types.ambiguity not in obj.defects