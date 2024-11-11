import pytest

from main.resources.AmbiguityErrorMessages import AmbiguityErrorMessages
from main.resources.AmbiguityErrorTypes import AmbiguityErrorTypes

@pytest.fixture
def ambiguity_defect_types():
    return AmbiguityErrorTypes()

@pytest.fixture
def ambiguity_error_messages():
    return AmbiguityErrorMessages()

def helper(response):
    """
    Transforms what is returned by the API to the expected format
    """
    defects = response.json
    transformed_defects = {}
    for defect in defects:
        transformed_defects[defect["title"]] = defect["description"]
    return transformed_defects

### NOTE: GOING VIA THE USER STORY ENDPOINT TO TEST THE AMBIGUITY STUFF BUT SAME THING OCCURS ON THE AC ENDPOINT ###


@pytest.mark.parametrize("story_text", [
    "As a system administrator, I want to allow only a few users to access a premium feature to control who has access.",
    "As a data analyst, I want to find a couple of duplicate entries in the database to clean up and optimize the data.",
    "As a marketing manager, I want to send an email to some users to target specific groups with promotions.",
    "Given I am logged in as a marketing manager, when I select a group of users and compose an email, then the email should be sent to some users."
])
def test_has_quantifiers_has_corresponding_issues_raised(test_client, ambiguity_defect_types, story_text):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert ambiguity_defect_types.ambiguity in data
    assert "quantifier" in "".join(data[ambiguity_defect_types.ambiguity])