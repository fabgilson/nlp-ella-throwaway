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


# Badly formed role
@pytest.mark.parametrize("story_text", [
    "As a aware, I want to be able to login to my account so that I can access my account.",
    "As a accessed i want to redesign the Resources page so that it matches the new Broker design styles.",
    "as a designed, I want to report to the Agencies about user testing, so that they are aware of their contributions to making Broker a better UX."
])
def test_roles_missing_nouns_have_only_missing_noun_defects(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.full_sentence in data
    assert len(data[user_story_defect_types.full_sentence]) == 1
    assert user_story_error_messages.role_doesnt_end_with_noun in data[user_story_defect_types.full_sentence]


@pytest.mark.parametrize("story_text", [
    "As a aware, so that I can access my account.",
    "As a accessed so that it matches the new Broker design styles.",
    "as a designed, so that they are aware of their contributions to making Broker a better UX."
])
def test_roles_missing_nouns_missing_means_have_correct_defects(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.full_sentence in data
    assert user_story_defect_types.well_formed in data
    assert len(data[user_story_defect_types.full_sentence]) == 1
    assert len(data[user_story_defect_types.well_formed]) == 1
    assert user_story_error_messages.role_doesnt_end_with_noun in data[user_story_defect_types.full_sentence]
    assert user_story_error_messages.missing_means in data[user_story_defect_types.well_formed]


@pytest.mark.parametrize("story_text", [
    "As a aware, I want to be able to login to my account",
    "As a accessed i want to redesign the Resources page",
    "as a designed, I want to report to the Agencies about user testing"
])
def test_roles_missing_nouns_missing_ends_have_correct_defects(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.full_sentence in data
    assert user_story_defect_types.well_formed in data
    assert len(data[user_story_defect_types.full_sentence]) == 1
    assert len(data[user_story_defect_types.well_formed]) == 1
    assert user_story_error_messages.role_doesnt_end_with_noun in data[user_story_defect_types.full_sentence]
    assert user_story_error_messages.missing_ends in data[user_story_defect_types.well_formed]


@pytest.mark.parametrize("story_text", [
    "aware, I want to be able to login to my account so that I can access my account.",
    "accessed i want to redesign the Resources page so that it matches the new Broker design styles.",
    "designed, I want to report to the Agencies about user testing, so that they are aware of their contributions to making Broker a better UX."
])
def test_roles_missing_nouns_missing_role_has_only_one_defect(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.well_formed in data
    assert len(data[user_story_defect_types.well_formed]) == 1
    assert user_story_error_messages.missing_role in data[user_story_defect_types.well_formed]


# Badly formed means
@pytest.mark.parametrize("story_text", [
    "As a user, I want to be able to login so that I can access my account.",
    "As a user i want to redesign so that it matches the new Broker design styles.",
    "As a user, I want to report, so that they are aware of their contributions to making Broker a better UX."
])
def test_means_missing_nouns_means_has_only_one_defect(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.full_sentence in data
    assert len(data[user_story_defect_types.full_sentence]) == 1
    assert user_story_error_messages.means_missing_noun in data[user_story_defect_types.full_sentence]


@pytest.mark.parametrize("story_text", [
    "As a user, I want account so that I can access my account.",
    "As a user i want a resources page so that it matches the new Broker design styles.",
    "As a user, I want user reports, so that they are aware of their contributions to making Broker a better UX."
])
def test_means_missing_verbs_means_has_only_one_defect(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.full_sentence in data
    assert len(data[user_story_defect_types.full_sentence]) == 1
    assert user_story_error_messages.means_missing_second_verb in data[user_story_defect_types.full_sentence]


@pytest.mark.parametrize("story_text", [
    "As a user, I want to so that I can access my account.",
    "As a user i want to so that it matches the new Broker design styles.",
    "As a user, I want to, so that they are aware of their contributions to making Broker a better UX."
])
def test_means_missing_verbs_and_nouns_means_has_two_defects(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.full_sentence in data
    assert len(data[user_story_defect_types.full_sentence]) == 2
    assert user_story_error_messages.means_missing_second_verb in data[user_story_defect_types.full_sentence]
    assert user_story_error_messages.means_missing_noun in data[user_story_defect_types.full_sentence]


@pytest.mark.parametrize("story_text", [
    "As a user, login to my account so that I can access my account.",
    "As a user redesign the page so that it matches the new Broker design styles.",
    "As a user, share user feedback so that they are aware of their contributions to making Broker a better UX."
])
def test_missing_means_verb_and_noun_only_has_one_defect(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.well_formed in data
    assert len(data[user_story_defect_types.well_formed]) == 1
    assert user_story_error_messages.missing_means in data[user_story_defect_types.well_formed]


@pytest.mark.parametrize("story_text", [
    "As a user, I want to login to my account so that.",
    "As a user, I want to redesign the page so that.",
    "As a user, I want to share the user feedback so that."
])
def test_ends_has_only_indicator(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.full_sentence in data
    assert user_story_error_messages.ends_missing_words in data[user_story_defect_types.full_sentence]