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
    "As a user, I want the system to send notifications as needed so that I am informed about important updates if applicable.",
    "As an admin, I want the system to apply security patches where feasible to ensure system integrity when necessary.",
    "As a project manager, I want to enable additional features if warranted by user demand, so that the project can evolve as circumstances dictate.",
    "As a user, I want to customize my dashboard layout if desired so that I can organize my workspace where appropriate.",
    "As a developer, I want to optimize code when possible to improve performance as far as practicable.",
    "Given a user has set notification preferences, When an important event occurs, Then the system should send a notification as needed, And only if applicable to the user's preferences.",
    "Given an admin is managing system security, When a new security patch is available, Then the system should apply the patch where feasible, And only when necessary to maintain system integrity."
])
def test_contains_escape_clauses_has_corresponding_defects(test_client, ambiguity_defect_types, story_text):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert ambiguity_defect_types.ambiguity in data
    assert "escape clause" in "".join(data[ambiguity_defect_types.ambiguity])