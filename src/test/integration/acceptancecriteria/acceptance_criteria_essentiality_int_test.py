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

# Check fine stories have no essential defects
@pytest.mark.parametrize("acs", [
    ["Given I connect to the system’s main URL, when I see the home page, then it includes a button labelled “Register”."],
    ["Given I am on the login form, when I click the ”Create an account” link, then I am taken to the registration page."],
    ["Given I am on my user profile page, when I see all my details, then I cannot edit any of the details that are shown to me."]
])
def test_essential_no_problems_have_no_essential_errors(test_client, acceptance_criteria_defect_types, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.essentiality not in data


@pytest.mark.parametrize("acs", [
    ["Given I connect to the system’s main URL, given I see the home page, then it includes a button labelled “Register”."],
    ["Given I am on the login form, when I click the “Not registered? Create an account” link, given I am taken to the registration page."],
    ["Given I am on my user profile page, given I see all my details, given I cannot edit any of the details that are shown to me."]
])
def test_essential_more_than_one_given_clause_has_appropriate_error(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.essentiality in data
    assert acceptance_criteria_error_messages.more_than_one_context in data[acceptance_criteria_defect_types.essentiality]


@pytest.mark.parametrize("acs", [
    ["When I connect to the system’s main URL, when I see the home page, then it includes a button labelled “Register”."],
    ["Given I am on the login form, when I click the “Not registered? Create an account” link, when I am taken to the registration page."],
    ["When I am on my user profile page, when I see all my details, when I cannot edit any of the details that are shown to me."]
])
def test_essential_more_than_one_when_clause_has_appropriate_error(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.essentiality in data
    assert acceptance_criteria_error_messages.more_than_one_event in data[acceptance_criteria_defect_types.essentiality]


@pytest.mark.parametrize("acs", [
    ["Then I connect to the system’s main URL, when I see the home page, then it includes a button labelled “Register”."],
    ["Given I am on the login form, then I click the “Not registered? Create an account” link, then I am taken to the registration page."],
    ["Then I am on my user profile page, then I see all my details, then I cannot edit any of the details that are shown to me."]
])
def test_essential_more_than_one_then_clause_has_appropriate_error(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.essentiality in data
    assert acceptance_criteria_error_messages.more_than_one_outcome in data[acceptance_criteria_defect_types.essentiality]

@pytest.mark.parametrize("acs", [
    ["Given I connect to the system’s main URL, when I see the home page, then it includes a button labelled “Register” (and I can click it)."],
    ["Given I am on the login form (on the system), when I click the ”Create an account” link, then I am taken to the registration page."],
    ["Given I am on my user profile page (and on the third tab), when I see all my details, then I cannot edit any of the details that are shown to me."]
])
def test_essential_acs_have_info_in_brackets_returns_expected_error(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.essentiality in data
    assert acceptance_criteria_error_messages.info_in_brackets in data[acceptance_criteria_defect_types.essentiality]

@pytest.mark.parametrize("acs", [
    ["Given I connect to the system’s main URL, when I see the home page, then it includes a button labelled “Register”. The button should be blue."],
    ["Given I am on the login form, when I click the ”Create an account” link, then I am taken to the registration page - this should be quick."],
    ["Given I am on my user profile page, when I see all my details, then I cannot edit any of the details that are shown to me * I also don't want to be able to see my password."]
])
def test_essential_acs_have_separating_punctuation_returns_expected_error(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.essentiality in data
    assert acceptance_criteria_error_messages.separating_punctuation in data[acceptance_criteria_defect_types.essentiality]

@pytest.mark.parametrize("acs", [
    ["Given I connect to the system’s main URL, when I see the home page e.g. the first page you see, then it includes a button labelled “Register”."],
    ["Given I am on the login form, when I click a button i.e. the ”Create an account” link, then I am taken to the registration page."],
    ["Given I am on my user profile page, when I see all my details eg. my name and email address, then I cannot edit any of the details that are shown to me."]
])
def test_essential_acs_have_example_indicators_not_marked_as_having_separating_punctuation(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.essentiality not in data

@pytest.mark.parametrize("acs", [
    ["Given I connect to the system’s main URL, when I see the home page, then it includes a button labelled “Register?”."],
    ["Given I am on the login form, when I click the ”Create an account.” link, then I am taken to the registration page."],
    ["Given I am on my user profile page, when I see all my details, then I can click a “Not my details - click for more info” button."]
])
def test_essential_acs_with_separating_punctuation_or_brackets_not_marked_as_not_essential(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.essentiality not in data


@pytest.mark.parametrize("acs", [
    ["Given I connect to the system’s main URL[1], when I see the home page, then it includes a button labelled “Register?”."],
    ["Given I am on the login form[2], when I click the ”Create an account.” link, then I am taken to the registration page."],
    ["Given I am on my user profile page, when I see all my details, then I can click a “Not my details - click for more info”[4] button."]
])
def test_essential_acs_with_references_in_square_brackets_are_ignored(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.essentiality not in data


@pytest.mark.parametrize("acs", [
    ["Given I am logged in, when I click on the “My Profile” button, then I am taken to a page with all my details i.e. my first and last names, date of birth (if given) and email address."],
    ["Given I am on the login form, when I click the ”Create an account.” link, then I am taken to the registration page (given I am not logged in)."],
    ["Given I am on my user profile page, when I see all my details, then I can click a “Not my details - click for more info” button (when I want to)."]
])
def test_essential_acs_indicators_in_brackets_not_marked_as_not_essential(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_error_messages.more_than_one_context not in data[acceptance_criteria_defect_types.essentiality]
    assert acceptance_criteria_error_messages.more_than_one_event not in data[acceptance_criteria_defect_types.essentiality]
    assert acceptance_criteria_error_messages.more_than_one_outcome not in data[acceptance_criteria_defect_types.essentiality]
