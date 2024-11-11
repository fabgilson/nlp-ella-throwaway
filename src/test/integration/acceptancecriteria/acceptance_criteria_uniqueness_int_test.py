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
    defects = response.json[-1]
    transformed_defects = {defects["title"]: defects["defects"]}
    return transformed_defects


# full duplicates
@pytest.mark.parametrize("acs", [
    ["Given I connect to the system’s main URL, when I see the home page, then it includes a button labelled “Register”.",
     "Given I Connect to the system’s main url, when I See the home page, then it includes a button labelled “Register”."],
    ["Given I am on the login form, when I click the ”Create an account” link, then I am taken to the registration page.",
     "Given I am on the login Form, when I click the ”Create an account” Link, then i am taken to the registration page."],
    ["Given I am on my user Profile page, when I see all my details, then i cannot edit any of the details that are shown to me.",
     "Given I am on my user profile page, when i see all my details, then I cannot edit any of the details That are shown to me."]
])
def test_identical_acs_returns_error(test_client, acceptance_criteria_defect_types, acceptance_criteria_error_messages, acs):
    response = test_client.post('/ac', json={"acceptance_criteria": acs})
    data = helper(response)
    assert response.status_code == 200
    assert acceptance_criteria_defect_types.uniqueness in data
    assert acceptance_criteria_error_messages.full_duplicates([0, 1]) in data[acceptance_criteria_defect_types.uniqueness]