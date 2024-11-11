import pytest
import os

from main.repositories.EscapeClauseRepository import EscapeClauseRepository
from main.repositories.NounExceptionRepository import NounExceptionRepository
from main.repositories.QuantifiersRespository import QuantifiersRepository
from main.repositories.VagueTermsRepository import VagueTermsRepository
from main.repositories.VerbExceptionRepository import VerbExceptionRepository
from main.repositories.VerbNounExceptionRepository import VerbNounExceptionRepository
from main.repositories.WeakVerbsRepository import WeakVerbsRepository
from main.resources.USErrorMessages import USErrorMessages
from main.resources.USErrorTypes import USErrorTypes
from main.services.NLPService import NLPService
from main.services.userstories.UserStoryPreprocessor import UserStoryPreprocessor
from main.services.WordlistService import WordlistService

@pytest.fixture
def user_story_defect_types():
    return USErrorTypes()

@pytest.fixture
def user_story_error_messages():
    return USErrorMessages()

@pytest.fixture
def user_story_preprocessor():
    base_path = os.path.dirname(os.path.realpath(__file__))
    noun_repo = NounExceptionRepository(base_path)
    verb_noun_repo = VerbNounExceptionRepository(base_path)
    verb_repo = VerbExceptionRepository(base_path)
    vague_repo = VagueTermsRepository(base_path)
    escape_repo = EscapeClauseRepository(base_path)
    quantifier_repo = QuantifiersRepository(base_path)
    weak_verbs_repository = WeakVerbsRepository(base_path)
    word_lists = WordlistService(verb_noun_repo, noun_repo, verb_repo, vague_repo, escape_repo, quantifier_repo, weak_verbs_repository)
    nlp_service = NLPService(word_lists)
    return UserStoryPreprocessor(nlp_service)

def helper(response):
    """
    Transforms what is returned by the API to the expected format
    """
    defects = response.json
    transformed_defects = {}
    for defect in defects:
        transformed_defects[defect["title"]] = defect["description"]
    return transformed_defects


# Check good user stories pass without defects
@pytest.mark.parametrize("story_text", [
    "As a user, I want to be able to login to my account so that I can access my account.",
    "As a UI designer i want to design the Resources page so that it matches the new Broker styles.",
    "as a UI designer, I want to report to the Agencies about user testing, so that they are aware of their contributions to making Broker a better UX."
])
def test_well_formed_user_stories_have_no_well_formed_defects(test_client, user_story_defect_types, story_text):
    response = test_client.post('/story', json={"story_text": story_text})
    assert response.status_code == 200
    assert user_story_defect_types.well_formed not in response.json

# Tests that the correct chunks are added to the user story object
@pytest.mark.parametrize("story_text", [
    "As a user, I want to be able to login so that I can access my account.",
    "As a UI designer i want to redesign the Resources page so that it matches the new Broker design styles.",
    "as a UI designer, I want to report to the Agencies about user testing, so that they are aware of their contributions to making Broker a better UX."
])
def test_well_formed_user_stories_have_correct_chunks(user_story_preprocessor, story_text):
    user_story, can_process = user_story_preprocessor.pre_process_story_text(story_text)
    assert user_story.role != None
    assert user_story.means != None
    assert user_story.ends != None
    assert can_process == True


@pytest.mark.parametrize("story_text", [
    "so that I can access my account details to read them.",
    "so that I can login to my account and see my details."
])
def test_stories_missing_role_and_means_have_correct_chunks(user_story_preprocessor, story_text):
    user_story, can_process = user_story_preprocessor.pre_process_story_text(story_text)
    assert user_story.role == None
    assert user_story.means == None
    assert user_story.ends != None
    assert can_process == True


@pytest.mark.parametrize("story_text", [
    "I want to be able to login to my account and see my details",
    "i want to redesign the Resources page to look more consistent",
    "I want to be able to report to the Agencies about user testing"
])
def test_stories_missing_role_and_ends_have_correct_chunks(user_story_preprocessor, story_text):
    user_story, can_process = user_story_preprocessor.pre_process_story_text(story_text)
    assert user_story.role == None
    assert user_story.ends == None
    assert user_story.means != None
    assert can_process == True


@pytest.mark.parametrize("story_text", [
    "As a Data user from this company,",
    "As a UI designer for this application",
    "as A senior Developer of this company's most popular application"
])
def test_stories_missing_means_and_ends_have_correct_chunks(user_story_preprocessor, story_text):
    user_story, can_process = user_story_preprocessor.pre_process_story_text(story_text)
    assert user_story.means == None
    assert user_story.ends == None
    assert user_story.role != None
    assert can_process == True


@pytest.mark.parametrize("story_text", [
    "it would be good to be able to login to the application",
    "it would be good to be able to register for the application",
    "could we please edit our details on our account page"
])
def test_stories_missing_role_means_and_ends_have_correct_chunks(user_story_preprocessor, story_text):
    user_story, can_process = user_story_preprocessor.pre_process_story_text(story_text)
    assert user_story.means == None
    assert user_story.ends == None
    assert user_story.role == None
    assert can_process == True


# Missing parts
@pytest.mark.parametrize("story_text", [
    "so that I can access my account and see my details.",
    "so that I can login to my account and see my details."
])
def test_stories_missing_role_and_means_have_two_well_formed_defects(test_client, user_story_defect_types, user_story_error_messages, story_text):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.well_formed in data
    assert len(data[user_story_defect_types.well_formed]) == 2
    assert user_story_error_messages.missing_role in data[user_story_defect_types.well_formed]
    assert user_story_error_messages.missing_means in data[user_story_defect_types.well_formed]


@pytest.mark.parametrize("story_text", [
    "I want to be able to login to my account and see my details",
    "i want to redesign the Resources page to be more consistent with what is already there",
    "I want to report to the Agencies about user testing and how well they are doing"
])
def test_stories_missing_role_and_ends_have_two_well_formed_defects(test_client, user_story_defect_types, user_story_error_messages, story_text):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.well_formed in data
    assert len(data[user_story_defect_types.well_formed]) == 2
    assert user_story_error_messages.missing_role in data[user_story_defect_types.well_formed]
    assert user_story_error_messages.missing_ends in data[user_story_defect_types.well_formed]


@pytest.mark.parametrize("story_text", [
    "As a Data user from this company,",
    "As a UI designer for this application",
    "as A senior Developer of this company's most popular application"
])
def test_stories_missing_means_and_ends_have_two_well_formed_defects(test_client, user_story_defect_types, user_story_error_messages, story_text):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.well_formed in data
    assert len(data[user_story_defect_types.well_formed]) == 2
    assert user_story_error_messages.missing_means in data[user_story_defect_types.well_formed]
    assert user_story_error_messages.missing_ends in data[user_story_defect_types.well_formed]


@pytest.mark.parametrize("story_text", [
   "it would be good to be able to login to the application",
    "it would be good to be able to register for the application",
    "could we please edit our details on our account page"
])
def test_stories_missing_means_role_and_ends_have_three_well_formed_defects(test_client, user_story_defect_types, user_story_error_messages, story_text):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.well_formed in data
    assert len(data[user_story_defect_types.well_formed]) == 3
    assert user_story_error_messages.missing_role in data[user_story_defect_types.well_formed]
    assert user_story_error_messages.missing_means in data[user_story_defect_types.well_formed]
    assert user_story_error_messages.missing_ends in data[user_story_defect_types.well_formed]


# Potential means
@pytest.mark.parametrize("story_text", [
    "As a user, I would like to login to my account so that I can access my account.",
    "As a user I would like to redesign the page so that it matches the new Broker design styles.",
    "As a user, I think it would be good to be able to share user feedback so that they are aware of their contributions to making Broker a better UX."
])
def test_potential_means_found_has_no_defects(test_client, user_story_defect_types, story_text):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.well_formed not in data


@pytest.mark.parametrize("story_text", [
    "I would like to login to my account so that I can access my account.",
    "I would like to redesign the page so that it matches the new Broker design styles.",
    "it would be good to be able to share user feedback so that they are aware of their contributions to making Broker a better UX."
])
def test_missing_role_no_means_is_found(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.well_formed in data
    assert len(data[user_story_defect_types.well_formed]) == 2
    assert user_story_error_messages.missing_means in data[user_story_defect_types.well_formed]
    assert user_story_error_messages.missing_role in data[user_story_defect_types.well_formed]


# Ordered role, means, ends
@pytest.mark.parametrize("story_text", [
    "I want to login As a user so that I can access my account",
    "I want to redesign the page so that it matches the new design As a user ",
    "so that UX team are aware of their contributions I want to be able to share user feedback as a dev",
    " as a dev so that UX team are aware of their contributions I want to be able to share user feedback",
])
def test_out_of_order_corresponding_defect_and_no_other_defects(test_client, user_story_defect_types, story_text, user_story_error_messages):
    response = test_client.post('/story', json={"story_text": story_text})
    data = helper(response)
    assert response.status_code == 200
    assert user_story_defect_types.well_formed in data
    assert len(data[user_story_defect_types.well_formed]) == 1
    assert user_story_error_messages.bad_ordering in data[user_story_defect_types.well_formed]
