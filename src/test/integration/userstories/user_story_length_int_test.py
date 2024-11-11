import pytest

from main.resources.USErrorMessages import USErrorMessages
from main.resources.USErrorTypes import USErrorTypes

@pytest.fixture
def user_story_defect_types():
    return USErrorTypes()

@pytest.fixture
def user_story_error_messages():
    return USErrorMessages(70)

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
    "As a user I want to login to my account so that I can access my account I can access my account I can access my account I can access my account I can access my account I can access my account I can access my account I can access my account  I can access my account  I can access my account  I can access my account  I can access my account I can access my account I can access my account I can access my account I can access my account.",
    "As a user I want to redesign the page so that it matches the new Broker design styles it matches the new Broker design styles it matches the new Broker design styles it matches the new Broker design styles it matches the new Broker design styles it matches the new Broker design styles it matches the new Broker design styles it matches the new Broker design styles it matches the new Broker design styles it matches the new Broker design styles it matches the new Broker design styles.",
    "as a dev I want to be able to share user feedback so that they are aware of their contributions to making Broker a better UX they are aware of their contributions to making Broker a better UX they are aware of their contributions to making Broker a better UX they are aware of their contributions to making Broker a better UX they are aware of their contributions to making Broker a better UX they are aware of their contributions to making Broker a better UX they are aware of their contributions to making Broker a better UX they are aware of their contributions to making Broker a better UX."
])
def test_stories_too_long_have_not_other_defects(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.length in data
    assert len(data[user_story_defect_types.length]) == 1
    assert user_story_error_messages.too_long in data[user_story_defect_types.length]