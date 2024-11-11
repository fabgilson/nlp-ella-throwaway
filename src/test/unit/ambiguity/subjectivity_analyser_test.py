import pytest

from unittest.mock import Mock

from main.models.UserStory import UserStory
from main.services.ambiguity.AmbiguityAnalyser import Subjectivity

@pytest.fixture
def subjectivity_analyser():
    return Subjectivity(Mock(), Mock(), Mock())

@pytest.fixture
def obj():
    return UserStory("", "")

# is subjective tests
def test_is_subjective_with_superlative(obj, subjectivity_analyser):
    subjectivity_analyser.has_superlatives_comparatives = Mock(return_value=([], ['best']))
    subjectivity_analyser.is_subjective(obj)
    assert subjectivity_analyser.ambiguity_types.ambiguity in obj.defects
    assert subjectivity_analyser.ambiguity_messages.superlative(['best']) in obj.defects[subjectivity_analyser.ambiguity_types.ambiguity]

def test_is_subjective_with_comparative(obj, subjectivity_analyser):
    subjectivity_analyser.has_superlatives_comparatives = Mock(return_value=(['better'], []))
    subjectivity_analyser.is_subjective(obj)
    assert subjectivity_analyser.ambiguity_types.ambiguity in obj.defects
    assert subjectivity_analyser.ambiguity_messages.comparative(['better']) in obj.defects[subjectivity_analyser.ambiguity_types.ambiguity]

def test_is_subjective_with_both(obj, subjectivity_analyser):
    subjectivity_analyser.has_superlatives_comparatives = Mock(return_value=(['better'], ['best']))
    subjectivity_analyser.is_subjective(obj)
    assert subjectivity_analyser.ambiguity_types.ambiguity in obj.defects
    assert subjectivity_analyser.ambiguity_messages.superlative(['best']) in obj.defects[subjectivity_analyser.ambiguity_types.ambiguity]
    assert subjectivity_analyser.ambiguity_messages.comparative(['better']) in obj.defects[subjectivity_analyser.ambiguity_types.ambiguity]

def test_is_subjective_with_neither(obj, subjectivity_analyser):
    subjectivity_analyser.has_superlatives_comparatives = Mock(return_value=([], []))
    subjectivity_analyser.is_subjective(obj)
    assert subjectivity_analyser.ambiguity_types.ambiguity not in obj.defects