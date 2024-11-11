import pytest

from unittest.mock import Mock
from main.models.AcceptanceCriteria import AcceptanceCriteria
from main.resources.ACErrorMessages import ACErrorMessages
from main.resources.ACErrorTypes import ACErrorTypes
from main.services.acceptancecriteria.AcceptanceCriteriaAnalyser import Singular

@pytest.fixture
def singular_analyser():
    return Singular(Mock(), ACErrorTypes(), ACErrorMessages())

@pytest.fixture
def acceptance_criteria_defect_types():
    return ACErrorTypes()

@pytest.fixture
def acceptance_criteria_error_messages():
    return ACErrorMessages()

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


# is singular tests
def test_is_singular_ac(singular_analyser, ac, acceptance_criteria_defect_types):
    singular_analyser.nlp_service.list_service.has_list_of_verbs = Mock(return_value=False)
    singular_analyser.nlp_service.check_for_lists = Mock(return_value=False) 
    singular_analyser.is_singular(ac)
    assert acceptance_criteria_defect_types.singularity not in ac.defects

def test_is_singular_context_has_list(singular_analyser, ac, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    singular_analyser.nlp_service.check_for_lists = Mock(side_effect=[True, False, False])
    singular_analyser.nlp_service.list_service.has_list_of_verbs = Mock(return_value=False)
    singular_analyser.is_singular(ac)
    assert acceptance_criteria_defect_types.singularity in ac.defects
    assert acceptance_criteria_error_messages.list_in_ac in ac.defects[acceptance_criteria_defect_types.singularity]

def test_is_singular_event_has_list(singular_analyser, ac, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    singular_analyser.nlp_service.check_for_lists = Mock(side_effect=[False, True, False])
    singular_analyser.nlp_service.list_service.has_list_of_verbs = Mock(return_value=False)
    singular_analyser.is_singular(ac)
    assert acceptance_criteria_defect_types.singularity in ac.defects
    assert acceptance_criteria_error_messages.list_in_ac in ac.defects[acceptance_criteria_defect_types.singularity]

def test_is_singular_outcome_has_list(singular_analyser, ac, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    singular_analyser.nlp_service.check_for_lists = Mock(side_effect=[False, False, True])
    singular_analyser.nlp_service.list_service.has_list_of_verbs = Mock(return_value=False)
    singular_analyser.is_singular(ac)
    assert acceptance_criteria_defect_types.singularity in ac.defects
    assert acceptance_criteria_error_messages.list_in_ac in ac.defects[acceptance_criteria_defect_types.singularity]