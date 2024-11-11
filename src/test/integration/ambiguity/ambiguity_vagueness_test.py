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
    "As a user, I want the application to provide adequate performance under various conditions, so that I can complete my tasks easily",
    "As a manager, I want the system to generate reports that are clear and similar to previous reports, so that they are easy to understand by all team members",
    "As an administrator, I need the system to offer strong security features, so that my organization's data is safe from potential threats.",
    "Given a user is logged in, When the user requests a report under various conditions, Then the system should generate a report with adequate performance, And the user should be able to complete the task easily.",
    "Given a manager has access to the report generation tool, When the manager generates a new report, Then the report should be similar to previous ones, And it should be clear and easy for all team members to understand.",
    "Given an administrator is configuring security settings, When the administrator selects the security options, Then the system should apply strong security features, And the data should be safe from potential threats."
])
def test_contains_vague_terms_has_corresponding_defects(test_client, ambiguity_defect_types, story_text):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert ambiguity_defect_types.ambiguity in data
    assert "vagueness" in "".join(data[ambiguity_defect_types.ambiguity])