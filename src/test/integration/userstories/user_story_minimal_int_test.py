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


# separating punctuation
@pytest.mark.parametrize("story_text", [
    "As a user, I want to be able to. login to my account so that I can access my account.",
    "As a UI designer i want to design the Resources; page so that it matches the new Broker styles.",
    "as a UI designer, I want? to report to the Agencies about user testing, so that they are aware of their contributions to making Broker a better UX."
])
def test_random_separating_punctuation_has_no_other_defects(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.minimal in data
    assert len(data[user_story_defect_types.minimal]) == 1
    assert user_story_error_messages.has_separating_punctuation in data[user_story_defect_types.minimal]


@pytest.mark.parametrize("story_text", [
    "As a user, I want to be able to login to my account so that I can access my account.",
    "As a UI designer i want to design the Resources page so that it matches the new Broker styles;",
    "as a UI designer, I want to report to the Agencies about user testing, so that they are aware of their contributions to making Broker a better UX?",
    "As a user, I want to browse through the list of facilities, so that I know my waste is not leaving a negative ecological footprint."
])
def test_ending_punctuation_has_no_defects(test_client, user_story_defect_types, story_text):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.minimal not in data


@pytest.mark.parametrize("story_text", [
    "As a user, I want to be able to login to my account so that I can access my account (and view details).",
    "As a UI designer i want to design the Resources page (among others) so that it matches the new Broker styles.",
    "as a UI designer, I want to report to the Agencies about user testing (and some other things), so that they are aware of their contributions to making Broker a better UX."
])
def test_brackets_containing_information_had_minimality_breach(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.minimal in data
    assert len(data[user_story_defect_types.minimal]) == 1
    assert user_story_error_messages.has_brackets in data[user_story_defect_types.minimal]


@pytest.mark.parametrize("story_text", [
    "As a user, I want to be able to login to my account so that I can access my account (and view details.",
    "As a UI designer i want to design the Resources page (among others so that it matches the new Broker styles.",
    "as a UI designer, I want to report to the Agencies about user testing (and some other things, so that they are aware of their contributions to making Broker a better UX."
    "as a user, I want to add a descriptions that can contain (, {, [ brackets, so that I can record a proper description."
])
def test_malformed_brackets_have_no_minimality_breach(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.minimal not in data