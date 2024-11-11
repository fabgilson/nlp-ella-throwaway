import pytest

from unittest.mock import Mock

from main.models.UserStory import UserStory
from main.services.ambiguity.AmbiguityAnalyser import Weakness

@pytest.fixture
def weakness_analyser():
    return Weakness(Mock(), Mock(), Mock(), Mock())

@pytest.fixture
def obj():
    return UserStory("", "")

# is weak
def test_is_weak_with_weak_verbs(weakness_analyser, obj):
    weakness_analyser.contains_weak_verbs = Mock(return_value=['should'])
    weakness_analyser.is_weak(obj)
    assert weakness_analyser.ambiguity_types.ambiguity in obj.defects
    assert weakness_analyser.ambiguity_messages.weakness(['should']) in obj.defects[weakness_analyser.ambiguity_types.ambiguity]

def test_is_weak_without_weak_verbs(weakness_analyser, obj):
    weakness_analyser.contains_weak_verbs = Mock(return_value=[])
    weakness_analyser.is_weak(obj)
    assert weakness_analyser.ambiguity_types.ambiguity not in obj.defects

# contains weak verbs
def test_contains_weak_verbs_with_weak_verbs(weakness_analyser, obj):
    text = "You could try to solve this problem, but you might not succeed."
    weakness_analyser.word_list_service.get_weak_verbs_list = Mock(return_value=['could', 'might'])
    weakness_analyser.nlp_service.tokenise_words = Mock(return_value=[
        ('You', 'PRP'), ('could', 'MD'), ('try', 'VB'), ('to', 'TO'),
        ('solve', 'VB'), ('this', 'DT'), ('problem', 'NN'),
        (',', ','), ('but', 'CC'), ('you', 'PRP'), ('might', 'MD'),
        ('not', 'RB'), ('succeed', 'VB')
    ])
    weakness_analyser.nlp_service.is_verb = Mock(return_value=True)
    weakness_analyser.nlp_service.is_modal = Mock(return_value=True)
    result = weakness_analyser.contains_weak_verbs(text)
    assert result == ['could', 'might']

def test_contains_verbs_but_not_in_list(weakness_analyser, obj):
    text = "You could try to solve this problem, but you might not succeed."
    weakness_analyser.word_list_service.get_weak_verbs_list = Mock(return_value=[])
    weakness_analyser.nlp_service.tokenise_words = Mock(return_value=[
        ('You', 'PRP'), ('could', 'MD'), ('try', 'VB'), ('to', 'TO'),
        ('solve', 'VB'), ('this', 'DT'), ('problem', 'NN'),
        (',', ','), ('but', 'CC'), ('you', 'PRP'), ('might', 'MD'),
        ('not', 'RB'), ('succeed', 'VB')
    ])
    weakness_analyser.nlp_service.is_verb = Mock(return_value=True)
    weakness_analyser.nlp_service.is_modal = Mock(return_value=True)
    result = weakness_analyser.contains_weak_verbs(text)
    assert result == []

def test_contains_weak_verbs_no_weak_verbs(weakness_analyser, obj):
    text = "You are trying to solve this problem effectively."
    weakness_analyser.word_list_service.get_weak_verbs_list = Mock(return_value=[])
    weakness_analyser.nlp_service.tokenise_words = Mock(return_value=[
        ('You', 'PRP'), ('are', 'VBP'), ('trying', 'VBG'), ('to', 'TO'),
        ('solve', 'VB'), ('this', 'DT'), ('problem', 'NN'),
        ('effectively', 'RB')
    ])
    weakness_analyser.nlp_service.is_verb = Mock(return_value=False)
    weakness_analyser.nlp_service.is_modal = Mock(return_value=False)
    result = weakness_analyser.contains_weak_verbs(text)
    assert result == []

def test_contains_weak_verbs_but_no_weak_verbs(weakness_analyser, obj):
    text = "You are trying to solve this problem effectively."
    weakness_analyser.word_list_service.get_weak_verbs_list = Mock(return_value=['trying'])
    weakness_analyser.nlp_service.tokenise_words = Mock(return_value=[
        ('You', 'PRP'), ('are', 'VBP'), ('trying', 'VBG'), ('to', 'TO'),
        ('solve', 'VB'), ('this', 'DT'), ('problem', 'NN'),
        ('effectively', 'RB')
    ])
    weakness_analyser.nlp_service.is_verb = Mock(return_value=False)
    weakness_analyser.nlp_service.is_modal = Mock(return_value=False)
    result = weakness_analyser.contains_weak_verbs(text)
    assert result == []

def test_contains_weak_verbs_empty_text(weakness_analyser, obj):
    text = ""
    weakness_analyser.nlp_service.tokenise_words = Mock(return_value=[])
    result = weakness_analyser.contains_weak_verbs(text)
    assert result == []