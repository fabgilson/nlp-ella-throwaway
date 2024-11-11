import pytest

from unittest.mock import Mock

from main.models.AcceptanceCriteria import AcceptanceCriteria
from main.resources.ACErrorMessages import ACErrorMessages
from main.resources.ACErrorTypes import ACErrorTypes
from main.services.acceptancecriteria.AcceptanceCriteriaPreprocessor import AcceptanceCriteriaPreprocessor

@pytest.fixture
def acceptance_criteria_preprocessor():
    return AcceptanceCriteriaPreprocessor(Mock())

@pytest.fixture
def acceptance_criteria_defect_types():
    return ACErrorTypes()

@pytest.fixture
def acceptance_criteria_error_messages():
    return ACErrorMessages()

@pytest.fixture
def valid_ac():
    return "Given address book is running, when I create a new address book, then address book contains 1 person"

@pytest.fixture
def ac_missing_context():
    return "when I create a new address book, then address book contains 1 person"

@pytest.fixture
def ac_missing_event():
    return "Given address book is running, then address book contains 1 person"

@pytest.fixture
def ac_missing_outcome():
    return "Given address book is running, when I create a new address book"

# extract context tests
def test_extract_context(acceptance_criteria_preprocessor, valid_ac):
    acceptance_criteria = AcceptanceCriteria(valid_ac.lower(), valid_ac)
    acceptance_criteria_preprocessor.extract_context(acceptance_criteria)
    assert acceptance_criteria.context == "given address book is running,"

def test_missing_context(acceptance_criteria_preprocessor, ac_missing_context, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    acceptance_criteria = AcceptanceCriteria(ac_missing_context.lower(), ac_missing_context)
    acceptance_criteria_preprocessor.find_user_persona_context = Mock(return_value=None)
    acceptance_criteria_preprocessor.extract_context(acceptance_criteria)
    assert acceptance_criteria.context is None
    assert acceptance_criteria_defect_types.integrous in acceptance_criteria.defects
    assert acceptance_criteria_error_messages.missing_context in acceptance_criteria.defects[acceptance_criteria_defect_types.integrous]

# extract event tests
def test_extract_event(acceptance_criteria_preprocessor, valid_ac):
    acceptance_criteria = AcceptanceCriteria(valid_ac.lower(), valid_ac)
    acceptance_criteria_preprocessor.extract_event(acceptance_criteria)
    assert acceptance_criteria.event == "when i create a new address book,"

def test_missing_event(acceptance_criteria_preprocessor, ac_missing_event, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    acceptance_criteria = AcceptanceCriteria(ac_missing_event.lower(), ac_missing_event)
    acceptance_criteria_preprocessor.extract_event(acceptance_criteria)
    assert acceptance_criteria.event is None
    assert acceptance_criteria_defect_types.integrous in acceptance_criteria.defects
    assert acceptance_criteria_error_messages.missing_event in acceptance_criteria.defects[acceptance_criteria_defect_types.integrous]

# extract outcome tests
def test_extract_outcome(acceptance_criteria_preprocessor, valid_ac):
    acceptance_criteria = AcceptanceCriteria(valid_ac.lower(), valid_ac)
    acceptance_criteria_preprocessor.extract_outcome(acceptance_criteria)
    assert acceptance_criteria.outcome == "then address book contains 1 person"


def test_missing_outcome(acceptance_criteria_preprocessor, ac_missing_outcome, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    acceptance_criteria = AcceptanceCriteria(ac_missing_outcome.lower(), ac_missing_outcome)
    acceptance_criteria_preprocessor.extract_outcome(acceptance_criteria)
    assert acceptance_criteria.outcome is None
    assert acceptance_criteria_defect_types.integrous in acceptance_criteria.defects
    assert acceptance_criteria.defects[acceptance_criteria_defect_types.integrous][0] == acceptance_criteria_error_messages.missing_outcome

# check ordering tests
def test_correct_order(acceptance_criteria_preprocessor, acceptance_criteria_defect_types):
    ac = AcceptanceCriteria(f"given address book is running, when i create a new address book, then address book contains 1 person", "")
    acceptance_criteria_preprocessor.nlp_service.remove_all_quotes_from_string = Mock(return_value=ac.original_lower_text)
    acceptance_criteria_preprocessor.remove_brackets = Mock(return_value=ac.original_lower_text)
    result = acceptance_criteria_preprocessor.check_context_event_outcome_ordering(ac)
    assert result
    assert acceptance_criteria_defect_types.integrous not in ac.defects

def test_incorrect_order(acceptance_criteria_preprocessor, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    ac = AcceptanceCriteria(f"when i create a new address book, given address book is running, then address book contains 1 person", "")
    acceptance_criteria_preprocessor.nlp_service.remove_all_quotes_from_string = Mock(return_value=ac.original_lower_text)
    acceptance_criteria_preprocessor.remove_brackets = Mock(return_value=ac.original_lower_text)
    result = acceptance_criteria_preprocessor.check_context_event_outcome_ordering(ac)
    assert not result
    assert acceptance_criteria_defect_types.integrous in ac.defects
    assert acceptance_criteria_error_messages.out_of_order in ac.defects[acceptance_criteria_defect_types.integrous]

def test_missing_event_correct_order(acceptance_criteria_preprocessor, acceptance_criteria_defect_types):
    ac = AcceptanceCriteria(f"given address book is running, then address book contains 1 person", "")
    acceptance_criteria_preprocessor.nlp_service.remove_all_quotes_from_string = Mock(return_value=ac.original_lower_text)
    acceptance_criteria_preprocessor.remove_brackets = Mock(return_value=ac.original_lower_text)
    result = acceptance_criteria_preprocessor.check_context_event_outcome_ordering(ac)
    assert result
    assert acceptance_criteria_defect_types.integrous not in ac.defects

def test_missing_event_incorrect_order(acceptance_criteria_preprocessor, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    ac = AcceptanceCriteria(f"then address book contains 1 person, given address book is running", "")
    acceptance_criteria_preprocessor.nlp_service.remove_all_quotes_from_string = Mock(return_value=ac.original_lower_text)
    acceptance_criteria_preprocessor.remove_brackets = Mock(return_value=ac.original_lower_text)
    result = acceptance_criteria_preprocessor.check_context_event_outcome_ordering(ac)
    assert not result
    assert acceptance_criteria_defect_types.integrous in ac.defects
    assert acceptance_criteria_error_messages.out_of_order in ac.defects[acceptance_criteria_defect_types.integrous]

def test_missing_outcome_correct_order(acceptance_criteria_preprocessor, acceptance_criteria_defect_types):
    ac = AcceptanceCriteria(f"given address book is running, when i create a new address book", "")
    acceptance_criteria_preprocessor.nlp_service.remove_all_quotes_from_string = Mock(return_value=ac.original_lower_text)
    acceptance_criteria_preprocessor.remove_brackets = Mock(return_value=ac.original_lower_text)
    result = acceptance_criteria_preprocessor.check_context_event_outcome_ordering(ac)
    assert result
    assert acceptance_criteria_defect_types.integrous not in ac.defects

def test_missing_outcome_incorrect_order(acceptance_criteria_preprocessor, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    ac = AcceptanceCriteria(f"when i create a new address book, given address book is running", "")
    acceptance_criteria_preprocessor.nlp_service.remove_all_quotes_from_string = Mock(return_value=ac.original_lower_text)
    acceptance_criteria_preprocessor.remove_brackets = Mock(return_value=ac.original_lower_text)
    result = acceptance_criteria_preprocessor.check_context_event_outcome_ordering(ac)
    assert not result
    assert acceptance_criteria_defect_types.integrous in ac.defects
    assert acceptance_criteria_error_messages.out_of_order in ac.defects[acceptance_criteria_defect_types.integrous]

def test_all_indicators_missing(acceptance_criteria_preprocessor, acceptance_criteria_defect_types):
    ac = AcceptanceCriteria(f"address book is running, i create a new address book, address book contains 1 person", "")
    acceptance_criteria_preprocessor.nlp_service.remove_all_quotes_from_string = Mock(return_value=ac.original_lower_text)
    acceptance_criteria_preprocessor.remove_brackets = Mock(return_value=ac.original_lower_text)
    result = acceptance_criteria_preprocessor.check_context_event_outcome_ordering(ac)
    assert result
    assert acceptance_criteria_defect_types.integrous not in ac.defects

# check there is only at most one of each indicator
def test_check_only_one_context_event_outcome_valid(acceptance_criteria_preprocessor, valid_ac, acceptance_criteria_defect_types):
    ac = AcceptanceCriteria(valid_ac, valid_ac)
    acceptance_criteria_preprocessor.nlp_service.remove_all_quotes_from_string = Mock(return_value=ac.original_lower_text)
    acceptance_criteria_preprocessor.remove_brackets = Mock(return_value=ac.original_lower_text)
    assert acceptance_criteria_preprocessor.check_only_one_context_event_outcome(ac)
    assert acceptance_criteria_defect_types.essentiality not in ac.defects

def test_check_only_one_context_event_outcome_multiple_context(acceptance_criteria_preprocessor, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    ac = AcceptanceCriteria("given i connect to the system’s main url, given i see the home page, then it includes a button labelled “register”.", "")
    acceptance_criteria_preprocessor.nlp_service.remove_all_quotes_from_string = Mock(return_value=ac.original_lower_text)
    acceptance_criteria_preprocessor.remove_brackets = Mock(return_value=ac.original_lower_text)
    assert not acceptance_criteria_preprocessor.check_only_one_context_event_outcome(ac)
    assert acceptance_criteria_defect_types.essentiality in ac.defects
    assert acceptance_criteria_error_messages.more_than_one_context in ac.defects[acceptance_criteria_defect_types.essentiality]

def test_check_only_one_context_event_outcome_multiple_event(acceptance_criteria_preprocessor, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    ac = AcceptanceCriteria("when i connect to the system’s main url, when i see the home page, then it includes a button labelled “register”.", "")
    acceptance_criteria_preprocessor.nlp_service.remove_all_quotes_from_string = Mock(return_value=ac.original_lower_text)
    acceptance_criteria_preprocessor.remove_brackets = Mock(return_value=ac.original_lower_text)
    assert not acceptance_criteria_preprocessor.check_only_one_context_event_outcome(ac)
    assert acceptance_criteria_defect_types.essentiality in ac.defects
    assert acceptance_criteria_error_messages.more_than_one_event in ac.defects[acceptance_criteria_defect_types.essentiality]

def test_check_only_one_context_event_outcome_multiple_outcome(acceptance_criteria_preprocessor, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    ac = AcceptanceCriteria("given i connect to the system’s main url, then i see the home page, then it includes a button labelled “register”.", "")
    acceptance_criteria_preprocessor.nlp_service.remove_all_quotes_from_string = Mock(return_value=ac.original_lower_text)
    acceptance_criteria_preprocessor.remove_brackets = Mock(return_value=ac.original_lower_text)
    assert not acceptance_criteria_preprocessor.check_only_one_context_event_outcome(ac)
    assert acceptance_criteria_defect_types.essentiality in ac.defects
    assert acceptance_criteria_error_messages.more_than_one_outcome in ac.defects[acceptance_criteria_defect_types.essentiality]

def test_check_only_one_context_event_outcome_multiple_violations(acceptance_criteria_preprocessor, acceptance_criteria_defect_types, acceptance_criteria_error_messages):
    ac = AcceptanceCriteria("given i connect to the system’s main url, given i see the home page, then i am on the home page, then it includes a button labelled “register”.", "")
    acceptance_criteria_preprocessor.nlp_service.remove_all_quotes_from_string = Mock(return_value=ac.original_lower_text)
    acceptance_criteria_preprocessor.remove_brackets = Mock(return_value=ac.original_lower_text)
    assert not acceptance_criteria_preprocessor.check_only_one_context_event_outcome(ac)
    assert acceptance_criteria_defect_types.essentiality in ac.defects
    assert acceptance_criteria_error_messages.more_than_one_outcome in ac.defects[acceptance_criteria_defect_types.essentiality]
    assert acceptance_criteria_error_messages.more_than_one_context in ac.defects[acceptance_criteria_defect_types.essentiality]

def test_indicator_inside_quotes_has_no_violations(acceptance_criteria_preprocessor, acceptance_criteria_defect_types):
    ac = AcceptanceCriteria("Given I am on the home page, when I click on the “given” button, then I see my profile", "")
    acceptance_criteria_preprocessor.nlp_service.remove_all_quotes_from_string = Mock(return_value="Given I am on the home page, when I click on the button, then I see my profile")
    acceptance_criteria_preprocessor.remove_brackets = Mock(return_value=ac.original_lower_text)
    assert acceptance_criteria_preprocessor.check_only_one_context_event_outcome(ac)
    assert acceptance_criteria_defect_types.essentiality not in ac.defects

# remove brackets text
def test_no_text_in_brackets_returns_same_text(acceptance_criteria_preprocessor):
    text_with_no_brackets = "Text with no brackets"
    acceptance_criteria_preprocessor.nlp_service.has_brackets_containing_information = Mock(return_value=[])
    assert acceptance_criteria_preprocessor.remove_brackets(text_with_no_brackets) == text_with_no_brackets

def test_text_in_brackets_returns_text_without_brackets(acceptance_criteria_preprocessor):
    text_with_no_brackets = "Text with brackets (containing more information)"
    expected = "Text with brackets ()"
    acceptance_criteria_preprocessor.nlp_service.has_brackets_containing_information = Mock(return_value=["containing more information"])
    assert acceptance_criteria_preprocessor.remove_brackets(text_with_no_brackets) == expected