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
    "As a user, I might want to update my profile information when there are any changes.",
    "As a project manager, I could ask for a progress report when the project timeline is at risk.",
    "As a developer, I may need to refactor the code when there are performance issues.",
    "Given the user is logged in, When they choose to update their profile information Then they might see a confirmation message if the update is successful",
    "Given the project timeline is at risk When the project manager requests a progress report Then the report could include recent updates and potential risks"
])
def test_contains_weak_verbs_has_corresponding_defects(test_client, ambiguity_defect_types, story_text):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert ambiguity_defect_types.ambiguity in data
    assert "weak" in "".join(data[ambiguity_defect_types.ambiguity])