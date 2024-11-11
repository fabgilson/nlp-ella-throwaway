import pytest

from unittest.mock import Mock
from main.models.UserStory import UserStory
from main.resources.USErrorMessages import USErrorMessages
from main.resources.USErrorTypes import USErrorTypes
from main.services.userstories.UserStoryAnalyser import FullSentence

@pytest.fixture
def user_story():
    return UserStory("text", "text")

@pytest.fixture
def full_sentence_analyser():
    return FullSentence(Mock(), USErrorTypes(), USErrorMessages())

@pytest.fixture
def user_story_defect_types():
    return USErrorTypes()

@pytest.fixture
def user_story_error_messages():
    return USErrorMessages()

# check role tests
def test_missing_noun_but_missing_role_not_reported_to_be_missing_noun(full_sentence_analyser, user_story, user_story_defect_types, user_story_error_messages):
    user_story.defects = {user_story_defect_types.well_formed: [user_story_error_messages.missing_role]}
    full_sentence_analyser.check_role_missing_noun = Mock(return_value=True)
    full_sentence_analyser.check_role(user_story)
    assert user_story_defect_types.full_sentence not in user_story.defects

def test_missing_noun_and_not_missing_role_reported_to_be_missing_noun(full_sentence_analyser, user_story, user_story_defect_types, user_story_error_messages):
    user_story.defects = {user_story_defect_types.well_formed: [user_story_error_messages.missing_means]}
    full_sentence_analyser.check_role_missing_noun = Mock(return_value=True)
    full_sentence_analyser.check_role(user_story)
    assert user_story_error_messages.role_doesnt_end_with_noun in user_story.defects[user_story_defect_types.full_sentence]

def test_missing_noun_and_full_sentence_reported_to_be_missing_noun(full_sentence_analyser, user_story, user_story_defect_types, user_story_error_messages):
    user_story.defects = {}
    full_sentence_analyser.check_role_missing_noun = Mock(return_value=True)
    full_sentence_analyser.check_role(user_story)
    assert user_story_error_messages.role_doesnt_end_with_noun in user_story.defects[user_story_defect_types.full_sentence]

def test_not_missing_noun_not_reported_to_be_missing_noun(full_sentence_analyser, user_story, user_story_defect_types, user_story_error_messages):
    user_story.defects = {}
    full_sentence_analyser.check_role_missing_noun = Mock(return_value=False)
    full_sentence_analyser.check_role(user_story)
    assert user_story_defect_types.full_sentence not in user_story.defects

# check role missing noun tests
def test_role_ends_with_noun_has_no_defects(full_sentence_analyser, user_story):
    user_story.role_pos = [('developer', 'NN')]
    full_sentence_analyser.nlp_service.is_noun = Mock(return_value=True)
    result = full_sentence_analyser.check_role_missing_noun(user_story.role_pos)
    assert not result

def test_role_does_not_end_with_noun(full_sentence_analyser, user_story):
    user_story.role_pos = [('developer', 'VERB')]
    full_sentence_analyser.nlp_service.is_noun = Mock(return_value=False)
    result = full_sentence_analyser.check_role_missing_noun(user_story.role_pos)
    assert result

def test_role_pos_empty_list_returns_true(full_sentence_analyser, user_story):
    user_story.role_pos = []
    result = full_sentence_analyser.check_role_missing_noun(user_story.role_pos)
    assert result

def test_role_with_no_pos_returns_true(full_sentence_analyser, user_story_defect_types, user_story_error_messages, user_story):
    user_story.role_pos = None
    result = full_sentence_analyser.check_role_missing_noun(user_story.role_pos)
    assert result


# check means tests
def test_means_missing_verb_reported_when_not_full_sentence_but_has_means(full_sentence_analyser, user_story, user_story_defect_types, user_story_error_messages):
    user_story.defects = {user_story_defect_types.well_formed: [user_story_error_messages.missing_role]}
    full_sentence_analyser.check_means_pos = Mock(return_value=(True, False))
    full_sentence_analyser.check_means_starts_with_i = Mock(return_value=True)
    full_sentence_analyser.check_means(user_story)
    assert user_story_error_messages.means_missing_second_verb in user_story.defects[user_story_defect_types.full_sentence]

def test_means_missing_noun_reported_when_not_full_sentence_but_has_means(full_sentence_analyser, user_story, user_story_defect_types, user_story_error_messages):
    user_story.defects = {user_story_defect_types.well_formed: [user_story_error_messages.missing_role]}
    full_sentence_analyser.check_means_pos = Mock(return_value=(False, True))
    full_sentence_analyser.check_means_starts_with_i = Mock(return_value=True)
    full_sentence_analyser.check_means(user_story)
    assert user_story_error_messages.means_missing_noun in user_story.defects[user_story_defect_types.full_sentence]

def test_means_missing_verb_reported_when_full_sentence(full_sentence_analyser, user_story, user_story_defect_types, user_story_error_messages):
    user_story.defects = {}
    full_sentence_analyser.check_means_pos = Mock(return_value=(True, False))
    full_sentence_analyser.check_means_starts_with_i = Mock(return_value=True)
    full_sentence_analyser.check_means(user_story)
    assert user_story_error_messages.means_missing_second_verb in user_story.defects[user_story_defect_types.full_sentence]

def test_means_missing_noun_reported_when_full_sentence(full_sentence_analyser, user_story, user_story_defect_types, user_story_error_messages):
    user_story.defects = {}
    full_sentence_analyser.check_means_pos = Mock(return_value=(False, True))
    full_sentence_analyser.check_means_starts_with_i = Mock(return_value=True)
    full_sentence_analyser.check_means(user_story)
    assert user_story_error_messages.means_missing_noun in user_story.defects[user_story_defect_types.full_sentence]

def test_means_no_issues_not_reported(full_sentence_analyser, user_story, user_story_defect_types):
    user_story.defects = {}
    full_sentence_analyser.check_means_pos = Mock(return_value=(False, False))
    full_sentence_analyser.check_means_starts_with_i = Mock(return_value=True)
    full_sentence_analyser.check_means(user_story)
    assert user_story_defect_types.full_sentence not in user_story.defects


# means POS tests
def test_means_pos_with_sufficient_verbs_and_nouns(full_sentence_analyser):
    pos = ['VB', 'VB', 'NN']
    full_sentence_analyser.nlp_service.has_required_number_verb_and_noun = Mock(return_value=(True, True))
    missing_verb, missing_noun = full_sentence_analyser.check_means_pos(pos)
    assert not missing_verb
    assert not missing_noun

def test_means_pos_with_insufficient_verbs(full_sentence_analyser):
    pos = ['VB', 'NN']
    full_sentence_analyser.nlp_service.has_required_number_verb_and_noun = Mock(return_value=(False, True))
    missing_verb, missing_noun = full_sentence_analyser.check_means_pos(pos)
    assert missing_verb
    assert not missing_noun

def test_means_pos_with_insufficient_nouns(full_sentence_analyser):
    pos = ['VB', 'VB']
    full_sentence_analyser.nlp_service.has_required_number_verb_and_noun = Mock(return_value=(True, False))
    missing_verb, missing_noun = full_sentence_analyser.check_means_pos(pos)
    assert not missing_verb
    assert missing_noun

def test_means_pos_with_insufficient_verbs_and_nouns(full_sentence_analyser):
    pos = ['NN']
    full_sentence_analyser.nlp_service.has_required_number_verb_and_noun = Mock(return_value=(False, False))
    missing_verb, missing_noun = full_sentence_analyser.check_means_pos(pos)
    assert missing_verb
    assert missing_noun