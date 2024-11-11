import pytest

from unittest.mock import Mock
from main.models.AcceptanceCriteria import AcceptanceCriteria
from main.resources.ACErrorMessages import ACErrorMessages
from main.resources.ACErrorTypes import ACErrorTypes
from main.services.acceptancecriteria.AcceptanceCriteriaAnalyser import Essential

@pytest.fixture
def acceptance_criteria():
    ac = AcceptanceCriteria("text", "text")
    ac.context = "text"
    ac.event = "text"
    ac.outcome = "text"
    return ac

@pytest.fixture
def essential_analyser():
    return Essential(Mock(), ACErrorTypes(), ACErrorMessages(), Mock())

@pytest.fixture
def acceptance_criteria_defect_types():
    return ACErrorTypes()

@pytest.fixture
def acceptance_criteria_error_messages():
    return ACErrorMessages()

# is essential tests
def test_is_essential_no_violations(essential_analyser, acceptance_criteria, acceptance_criteria_defect_types):
    essential_analyser.nlp_service.has_separating_punctuation_with_following_text = Mock(return_value=False)
    essential_analyser.nlp_service.has_brackets_containing_information = Mock(return_value=[])    
    essential_analyser.is_essential(acceptance_criteria)
    assert acceptance_criteria_defect_types.essentiality not in acceptance_criteria.defects

def test_is_essential_separating_punctuation_violation(essential_analyser, acceptance_criteria, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    essential_analyser.nlp_service.has_separating_punctuation_with_following_text = Mock(return_value=True)
    essential_analyser.nlp_service.has_brackets_containing_information = Mock(return_value=[])    
    essential_analyser.is_essential(acceptance_criteria)
    assert acceptance_criteria_defect_types.essentiality in acceptance_criteria.defects
    assert len(acceptance_criteria.defects[acceptance_criteria_defect_types.essentiality]) == 1
    assert acceptance_criteria_error_messages.separating_punctuation in acceptance_criteria.defects[acceptance_criteria_defect_types.essentiality]

def test_is_essential_brackets_violation(essential_analyser, acceptance_criteria, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    essential_analyser.nlp_service.has_separating_punctuation_with_following_text = Mock(return_value=False)
    essential_analyser.nlp_service.has_brackets_containing_information = Mock(return_value=["violation"])    
    essential_analyser.is_essential(acceptance_criteria)
    assert acceptance_criteria_defect_types.essentiality in acceptance_criteria.defects
    assert len(acceptance_criteria.defects[acceptance_criteria_defect_types.essentiality]) == 1
    assert acceptance_criteria_error_messages.info_in_brackets in acceptance_criteria.defects[acceptance_criteria_defect_types.essentiality]

def test_is_essential_both_violations(essential_analyser, acceptance_criteria, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    essential_analyser.nlp_service.has_separating_punctuation_with_following_text = Mock(return_value=True)
    essential_analyser.nlp_service.has_brackets_containing_information = Mock(return_value=["violation"])    
    essential_analyser.is_essential(acceptance_criteria)
    assert acceptance_criteria_defect_types.essentiality in acceptance_criteria.defects
    assert len(acceptance_criteria.defects[acceptance_criteria_defect_types.essentiality]) == 2
    assert acceptance_criteria_error_messages.info_in_brackets in acceptance_criteria.defects[acceptance_criteria_defect_types.essentiality]
    assert acceptance_criteria_error_messages.separating_punctuation in acceptance_criteria.defects[acceptance_criteria_defect_types.essentiality]

