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
    "As a user and as a writer I want to login to my account so that I can access my account and see their details.",
    "As a user and as a developer I want to redesign the page so that it matches the new Broker design styles.",
    "as a dev and as a user I want to be able to share user feedback so that they are aware of contributions to making Broker."
])
def test_anaphora_has_corresponding_issues_raised(test_client, ambiguity_defect_types, story_text):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert ambiguity_defect_types.ambiguity in data
    assert "anaphora" in "".join(data[ambiguity_defect_types.ambiguity])