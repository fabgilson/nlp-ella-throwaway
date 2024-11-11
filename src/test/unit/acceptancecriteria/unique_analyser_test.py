import pytest

from unittest.mock import Mock
from main.models.AcceptanceCriteria import AcceptanceCriteria
from main.resources.ACErrorMessages import ACErrorMessages
from main.resources.ACErrorTypes import ACErrorTypes
from main.services.acceptancecriteria.AcceptanceCriteriaAnalyser import Unique

@pytest.fixture
def unique_analyser():
    return Unique(Mock(), ACErrorTypes(), ACErrorMessages())

@pytest.fixture
def acceptance_criteria_defect_types():
    return ACErrorTypes()

@pytest.fixture
def acceptance_criteria_error_messages():
    return ACErrorMessages()

@pytest.fixture
def acs():
    ac = AcceptanceCriteria("text", "text")
    return [ac]

# are unique tests
def test_are_unique_no_duplicates(unique_analyser, acs):
    unique_analyser.has_full_duplicates = Mock(return_value={})
    defects = unique_analyser.are_unique(acs)
    assert len(defects) == 0

def test_are_unique_with_duplicates(unique_analyser, acs, acceptance_criteria_error_messages):
    full_duplicates = {'duplicate text': [0, 2]}
    unique_analyser.has_full_duplicates = Mock(return_value=full_duplicates)
    defects = unique_analyser.are_unique(acs)
    expected_error = acceptance_criteria_error_messages.full_duplicates([0, 2])
    assert len(defects) == 1
    assert defects[0] == expected_error

# has full duplicate tests
def test_has_full_duplicates(unique_analyser):
    acs = ['text1', 'text2', 'text1', 'text3', 'text2']
    expected_duplicates = {
        'text1': [0, 2],
        'text2': [1, 4]
    }
    duplicates = unique_analyser.has_full_duplicates(acs)
    assert duplicates == expected_duplicates