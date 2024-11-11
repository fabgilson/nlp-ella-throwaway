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
    "As a user and as a writer I want to login to my account so that I can access my account.",
    "As a user and as a developer I want to redesign the page so that it matches the new Broker design styles.",
    "as a dev and as a user I want to be able to share user feedback so that they are aware of their contributions to making Broker a better UX."
])
def test_more_than_one_role_has_corresponding_defect_and_no_other_defects(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.atomic in data
    assert len(data[user_story_defect_types.atomic]) == 1
    assert user_story_error_messages.more_than_one_role in data[user_story_defect_types.atomic]


@pytest.mark.parametrize("story_text", [
    "As a user I want to login to my account and I want to view my details.",
    "As a user I want to redesign the page and I want it to match the new Broker design.",
    "as a dev I want to be able to share user feedback and I want Broker to be aware of their contributions."
])
def test_more_than_one_means_has_corresponding_defect_and_no_other_defects(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.atomic in data
    assert len(data[user_story_defect_types.atomic]) == 1
    assert user_story_error_messages.more_than_one_means in data[user_story_defect_types.atomic]


@pytest.mark.parametrize("story_text", [
    "As a user or developer I want to login so that I can access my account",
    "As a user and admin I want to redesign the page so that it matches the new design",
    "as a developer + user I want to be able to share user feedback so that UX team are aware of their contributions",
    "As a user / developer I want to login so that I can access my account",
    "As a user & developer I want to login so that I can access my account",
    "As a user < developer I want to login so that I can access my account",
])
def test_role_with_conjuctions_is_not_atomic(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.atomic in data
    assert len(data[user_story_defect_types.atomic]) == 1
    assert user_story_error_messages.more_than_one_role in data[user_story_defect_types.atomic]


@pytest.mark.parametrize("story_text", [
    "As a user I want to login to my account + see my account so that I can update my account",
    "As a user I want to redesign the page & update its interface so that it matches the new design",
    "as a dev I want to be able to share user feedback / hear their ideas so that UX team are aware of their contribution",
    "As a user I want to login to my account and see my account",
    "As a user I want to login to my account or see my account",
])
def test_means_with_conjuctions_is_not_atomic(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.atomic in data
    assert len(data[user_story_defect_types.atomic]) == 1
    assert user_story_error_messages.more_than_one_means in data[user_story_defect_types.atomic]


