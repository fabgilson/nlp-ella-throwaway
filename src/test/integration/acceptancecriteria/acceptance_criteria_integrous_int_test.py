import pytest

from main.resources.ACErrorMessages import ACErrorMessages
from main.resources.ACErrorTypes import ACErrorTypes

@pytest.fixture
def acceptance_criteria_defect_types():
    return ACErrorTypes()

@pytest.fixture
def acceptance_criteria_error_messages():
    return ACErrorMessages()

def helper(response):
    """
    Transforms response into expected format
    """
    defects = response.json[0]["defects"]
    transformed_defects = {}
    for defect in defects:
        transformed_defects[defect["title"]] = defect["descriptions"]
    return transformed_defects

# Check fine stories have no integrous defects
@pytest.mark.parametrize("acs", [
    ["Given I connect to the system’s main URL, when I see the home page, then it includes a button labelled “Register”."],
    ["Given I am on the login form, when I click the “Not registered? Create an account” link, then I am taken to the registration page."],
    ["Given I am on my user profile page, when I see all my details, then I cannot edit any of the details that are shown to me."]
])
def test_integral_acs_have_no_integrous_defects(test_client, acceptance_criteria_defect_types, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.integrous not in data


@pytest.mark.parametrize("acs", [
    ["Given I connect to the system’s main URL, when I see the home page."],
    ["Given I am on the login form, when I click the “Not registered? Create an account” link."],
    ["Given I am on the login form, when I click the “Cancel” button."]
])
def test_acs_missing_then_clause_have_integrous_defects(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.integrous in data
    assert acceptance_criteria_error_messages.missing_outcome in data[acceptance_criteria_defect_types.integrous]


@pytest.mark.parametrize("acs", [
    ["then it includes a button labelled “Register”."],
    ["then it contains the text “Not registered? Create an account” which is highlighted as a link."],
    ["then I cannot access or modify any other user's profile."]
])
def test_acs_missing_given_and_when_clauses_have_integrous_defects(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.integrous in data
    assert acceptance_criteria_error_messages.missing_context in data[acceptance_criteria_defect_types.integrous] 
    assert acceptance_criteria_error_messages.missing_event in data[acceptance_criteria_defect_types.integrous] 


# check ordering
@pytest.mark.parametrize("acs", [
    ["when i create a new address book, given address book is running"],
    ["then address book contains 1 person, given address book is running"],
    ["when i create a new address book, given address book is running, then address book contains 1 person"],
])
def test_out_of_order_corresponding_defect_and_no_other_defects(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.integrous in data
    assert len(data[acceptance_criteria_defect_types.integrous]) == 1
    assert acceptance_criteria_error_messages.out_of_order in data[acceptance_criteria_defect_types.integrous]


# check POS
@pytest.mark.parametrize("acs", [
    ["when i create a new address book, given address book"],
    ["then address book contains 1 person, given address book"],
    ["when i create a new address book, given address book, then address book contains 1 person"],
])
def test_out_of_order_and_bad_pos_no_pos_errors(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.integrous in data
    assert len(data[acceptance_criteria_defect_types.integrous]) == 1
    assert acceptance_criteria_error_messages.out_of_order in data[acceptance_criteria_defect_types.integrous]
    assert acceptance_criteria_error_messages.context_missing_noun_or_verb not in data[acceptance_criteria_defect_types.integrous]


@pytest.mark.parametrize("acs", [
    ["Given the system’s main URL, when I see the home page, then it includes a button labelled “Register”."],
    ["Given the registration form, when I click the “Cancel” button, then I am taken back to the system’s home page"],
    ["Given my user profile page, when I see all my details, then I cannot edit any of the details that are shown to me."]
])
def test_context_missing_required_pos(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.integrous in data
    assert len(data[acceptance_criteria_defect_types.integrous]) == 1
    assert acceptance_criteria_error_messages.context_missing_noun_or_verb in data[acceptance_criteria_defect_types.integrous]


@pytest.mark.parametrize("acs", [
    ["Given I connect to the system’s main URL, when the home page, then it includes a button labelled “Register”."],
    ["Given I am on the registration form, when the “Cancel” button, then I am taken back to the system’s home page"],
    ["Given I am on my user profile page, when all my details, then I cannot edit any of the details that are shown to me."]
])
def test_event_missing_required_pos(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.integrous in data
    assert len(data[acceptance_criteria_defect_types.integrous]) == 1
    assert acceptance_criteria_error_messages.event_missing_noun_or_verb in data[acceptance_criteria_defect_types.integrous]


@pytest.mark.parametrize("acs", [
    ["Given I connect to the system’s main URL, when I see the home page, then a button “Register”."],
    ["Given I am on the registration form, when I click the “Cancel” button, then the system’s home page"],
    ["Given I am on my user profile page, when I see all my details, then the details"]
])
def test_outcome_missing_required_pos(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.integrous in data
    assert len(data[acceptance_criteria_defect_types.integrous]) == 1
    assert acceptance_criteria_error_messages.outcome_missing_noun_or_verb in data[acceptance_criteria_defect_types.integrous]