import pytest

from unittest.mock import Mock
from main.models.AcceptanceCriteria import AcceptanceCriteria
from main.resources.ACErrorMessages import ACErrorMessages
from main.resources.ACErrorTypes import ACErrorTypes
from main.services.acceptancecriteria.AcceptanceCriteriaAnalyser import Integrous

@pytest.fixture
def acceptance_criteria():
    ac = AcceptanceCriteria("text", "text")
    ac.context = "text"
    ac.event = "text"
    ac.outcome = "text"
    return ac

@pytest.fixture
def integrous_analyser():
    return Integrous(Mock(), ACErrorTypes(), ACErrorMessages())

@pytest.fixture
def acceptance_criteria_defect_types():
    return ACErrorTypes()

@pytest.fixture
def acceptance_criteria_error_messages():
    return ACErrorMessages()

# POS checks
def test_is_integrous_context_bad_pos(acceptance_criteria, integrous_analyser, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    integrous_analyser.nlp_service.has_required_number_verb_and_noun = Mock(side_effect=[(False, False), (True, True), (True, True)])
    integrous_analyser.is_integrous(acceptance_criteria)
    assert acceptance_criteria_defect_types.integrous in acceptance_criteria.defects
    assert len(acceptance_criteria.defects[acceptance_criteria_defect_types.integrous]) == 1
    assert acceptance_criteria_error_messages.context_missing_noun_or_verb in acceptance_criteria.defects[acceptance_criteria_defect_types.integrous]

def test_is_integrous_event_bad_pos(acceptance_criteria, integrous_analyser, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    integrous_analyser.nlp_service.has_required_number_verb_and_noun = Mock(side_effect=[(True, True), (False, False), (True, True)])
    integrous_analyser.is_integrous(acceptance_criteria)
    assert acceptance_criteria_defect_types.integrous in acceptance_criteria.defects
    assert len(acceptance_criteria.defects[acceptance_criteria_defect_types.integrous]) == 1
    assert acceptance_criteria_error_messages.event_missing_noun_or_verb in acceptance_criteria.defects[acceptance_criteria_defect_types.integrous]

def test_is_integrous_outcome_bad_pos(acceptance_criteria, integrous_analyser, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    integrous_analyser.nlp_service.has_required_number_verb_and_noun = Mock(side_effect=[(True, True), (True, True), (False, False)])
    integrous_analyser.is_integrous(acceptance_criteria)
    assert acceptance_criteria_defect_types.integrous in acceptance_criteria.defects
    assert len(acceptance_criteria.defects[acceptance_criteria_defect_types.integrous]) == 1
    assert acceptance_criteria_error_messages.outcome_missing_noun_or_verb in acceptance_criteria.defects[acceptance_criteria_defect_types.integrous]

def test_is_integrous_bad_pos_but_missing_context(acceptance_criteria, integrous_analyser, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    integrous_analyser.nlp_service.has_required_number_verb_and_noun = Mock(side_effect=[(False, False), (True, True), (True, True)])
    acceptance_criteria.context = None
    integrous_analyser.is_integrous(acceptance_criteria)
    assert acceptance_criteria_defect_types.integrous not in acceptance_criteria.defects

def test_is_integrous_bad_pos_but_missing_event(acceptance_criteria, integrous_analyser, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    integrous_analyser.nlp_service.has_required_number_verb_and_noun = Mock(side_effect=[(True, True), (False, False), (True, True)])
    acceptance_criteria.event = None
    integrous_analyser.is_integrous(acceptance_criteria)
    assert acceptance_criteria_defect_types.integrous not in acceptance_criteria.defects

def test_is_integrous_bad_pos_but_missing_outcome(acceptance_criteria, integrous_analyser, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    integrous_analyser.nlp_service.has_required_number_verb_and_noun = Mock(side_effect=[(True, True), (True, True), (False, False)])
    acceptance_criteria.outcome = None
    integrous_analyser.is_integrous(acceptance_criteria)
    assert acceptance_criteria_defect_types.integrous not in acceptance_criteria.defects