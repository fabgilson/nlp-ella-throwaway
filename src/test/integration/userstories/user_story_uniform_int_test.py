import pytest

from main.resources.USErrorMessages import USErrorMessages
from main.resources.USErrorTypes import USErrorTypes

@pytest.fixture
def user_story_defect_types():
    return USErrorTypes()

@pytest.fixture
def user_story_error_messages():
    return USErrorMessages()

def helper(response):
    """
    Transforms what is returned by the API to the expected format
    """
    defects = response.json
    transformed_defects = {}
    for defect in defects:
        transformed_defects[defect["title"]] = defect["description"]
    return transformed_defects


@pytest.mark.parametrize("story_text", [
    "As a user I would like to login to my account so that I can access my account.",
    "As a UI designer i want to design the Resources page so it matches the new Broker UI.",
    "Here as a designer, I want to report to the Agencies about user testing, so that they are aware of their contributions to making Broker a better UX."
])
def test_otherwise_well_written_stories_have_uniform_error(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert data
    assert user_story_defect_types.uniform in data
    assert user_story_error_messages.not_uniform in data[user_story_defect_types.uniform]