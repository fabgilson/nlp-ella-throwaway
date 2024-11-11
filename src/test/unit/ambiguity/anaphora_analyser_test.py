import pytest

from unittest.mock import Mock

from main.models.UserStory import UserStory
from main.services.ambiguity.AmbiguityAnalyser import Anaphora

@pytest.fixture
def anaphora_analyser():
    return Anaphora(Mock(), Mock(), Mock())

@pytest.fixture
def obj():
    return UserStory("", "")

def test_has_anaphora_with_anaphora(anaphora_analyser, obj):
    anaphora_analyser.contains_anaphora_indicators = Mock(return_value=['she'])
    anaphora_analyser.has_anaphora(obj)
    assert anaphora_analyser.ambiguity_types.ambiguity in obj.defects
    assert anaphora_analyser.ambiguity_messages.anaphora(['she']) in obj.defects[anaphora_analyser.ambiguity_types.ambiguity]

def test_has_anaphora_without_anaphora(anaphora_analyser, obj):
    anaphora_analyser.contains_anaphora_indicators = Mock(return_value=[])
    anaphora_analyser.has_anaphora(obj)
    assert anaphora_analyser.ambiguity_types.ambiguity not in obj.defects

def test_has_anaphora_with_multiple_anaphora(anaphora_analyser, obj):
    anaphora_analyser.contains_anaphora_indicators = Mock(return_value=['she', 'her', 'its'])
    anaphora_analyser.has_anaphora(obj)
    assert anaphora_analyser.ambiguity_types.ambiguity in obj.defects
    assert anaphora_analyser.ambiguity_messages.anaphora(['she', 'her', 'its']) in obj.defects[anaphora_analyser.ambiguity_types.ambiguity]