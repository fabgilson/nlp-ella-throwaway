import pytest

from unittest.mock import Mock
from main.models.UserStory import UserStory
from main.resources.USErrorMessages import USErrorMessages
from main.resources.USErrorTypes import USErrorTypes
from main.services.userstories.UserStoryPreprocessor import UserStoryPreprocessor
from main.types.UserStoryParts import UserStoryPart

@pytest.fixture
def user_story_preprocessor():
    return UserStoryPreprocessor(Mock())

@pytest.fixture
def user_story_defect_types():
    return USErrorTypes()

@pytest.fixture
def user_story_error_messages():
    return USErrorMessages(70)

@pytest.fixture
def valid_story():
    return "As a user, I want to be able to login so that I can access my account."

@pytest.fixture
def ends():
    return "so that I can access my account."

@pytest.fixture
def means():
    return "I want to be able to login"

@pytest.fixture
def story_missing_role():
    return "I want to be able to login so that I can access my account."

@pytest.fixture
def story_missing_means():
    return "As a user, so that I can access my account."

@pytest.fixture
def story_missing_ends():
    return "As a user, I want to be able to login"

@pytest.fixture
def pos_list():
    return [('This', 'DT'), ('is', 'VBZ'), ('a', 'DT'), ('test', 'NN')]

@pytest.fixture
def pos_text():
    return "This is a test"

# preprocess story text
def test_pre_process_story_text(user_story_preprocessor, valid_story):
    user_story_preprocessor.check_only_one_role_means_ends = Mock(return_value=True)
    user_story_preprocessor.check_role_means_ends_ordering = Mock(return_value=True)
    user_story_preprocessor.has_okay_length = Mock(return_value=True)
    user_story_preprocessor.split_story_into_chunks = Mock()
    user_story_preprocessor.tokenise_and_pos_tag_chunk = Mock()
    user_story, can_process = user_story_preprocessor.pre_process_story_text(valid_story)
    assert user_story.original_lower_text == valid_story.lower()
    assert can_process

def test_pre_process_story_text_cant_process_because_out_of_order(user_story_preprocessor, valid_story):
    user_story_preprocessor.check_only_one_role_means_ends = Mock(return_value=True)
    user_story_preprocessor.check_role_means_ends_ordering = Mock(return_value=False)
    user_story_preprocessor.has_okay_length = Mock(return_value=True)
    user_story, can_process = user_story_preprocessor.pre_process_story_text(valid_story)
    assert user_story.original_lower_text == valid_story.lower()
    assert not can_process

def test_pre_process_story_text_cant_process_because_more_than_one_chunk(user_story_preprocessor, valid_story):
    user_story_preprocessor.check_only_one_role_means_ends = Mock(return_value=False)
    user_story_preprocessor.check_role_means_ends_ordering = Mock(return_value=True)
    user_story_preprocessor.has_okay_length = Mock(return_value=True)
    user_story, can_process = user_story_preprocessor.pre_process_story_text(valid_story)
    assert user_story.original_lower_text == valid_story.lower()
    assert not can_process

def test_pre_process_story_text_cant_process_because_wrong_length(user_story_preprocessor, valid_story):
    user_story_preprocessor.check_only_one_role_means_ends = Mock(return_value=True)
    user_story_preprocessor.check_role_means_ends_ordering = Mock(return_value=True)
    user_story_preprocessor.has_okay_length = Mock(return_value=False)
    user_story, can_process = user_story_preprocessor.pre_process_story_text(valid_story)
    assert user_story.original_lower_text == valid_story.lower()
    assert not can_process

# only one role, means, and ends test
def test_check_only_one_role_means_ends_valid(user_story_preprocessor, valid_story, user_story_defect_types, user_story_error_messages):
    story = UserStory(valid_story, valid_story)
    assert user_story_preprocessor.check_only_one_role_means_ends(story)
    assert user_story_defect_types.atomic not in story.defects

def test_check_only_one_role_means_ends_multiple_means(user_story_preprocessor, user_story_defect_types, user_story_error_messages):
    story = UserStory("as a user i want to log in so that i can access my account i want to reset my password", "")
    assert not user_story_preprocessor.check_only_one_role_means_ends(story)
    assert user_story_defect_types.atomic in story.defects
    assert user_story_error_messages.more_than_one_means in story.defects[user_story_defect_types.atomic]

def test_check_only_one_role_means_ends_multiple_ends(user_story_preprocessor, user_story_defect_types, user_story_error_messages):
    story = UserStory("as a user i want to log in so that i can access my account so that i can change my settings", "")
    assert not user_story_preprocessor.check_only_one_role_means_ends(story)
    assert user_story_defect_types.atomic in story.defects
    assert user_story_error_messages.more_than_one_ends in story.defects[user_story_defect_types.atomic]

def test_check_only_one_role_means_ends_multiple_violations(user_story_preprocessor, user_story_defect_types, user_story_error_messages):
    story = UserStory("as a guest i want to log in and i want to see my details so that i can access my account so that i can change my settings", "")
    assert not user_story_preprocessor.check_only_one_role_means_ends(story)
    assert user_story_defect_types.atomic in story.defects
    assert user_story_error_messages.more_than_one_ends in story.defects[user_story_defect_types.atomic]
    assert user_story_error_messages.more_than_one_means in story.defects[user_story_defect_types.atomic]

# check ordering tests
def test_correct_order(user_story_preprocessor, user_story_defect_types):
    story = UserStory(f"as a user I want to log in so that i can access my account", "")
    result = user_story_preprocessor.check_role_means_ends_ordering(story)
    assert result
    assert user_story_defect_types.well_formed not in story.defects

def test_incorrect_order(user_story_preprocessor, user_story_defect_types, user_story_error_messages):
    story = UserStory(f"i want to log in as a user so that i can access my account", "")
    result = user_story_preprocessor.check_role_means_ends_ordering(story)
    assert not result
    assert user_story_defect_types.well_formed in story.defects
    assert user_story_error_messages.bad_ordering in story.defects[user_story_defect_types.well_formed]

def test_missing_means_correct_order(user_story_preprocessor, user_story_defect_types):
    story = UserStory(f"as a user so that i can access my account", "")
    result = user_story_preprocessor.check_role_means_ends_ordering(story)
    assert result
    assert user_story_defect_types.well_formed not in story.defects

def test_missing_means_incorrect_order(user_story_preprocessor, user_story_defect_types, user_story_error_messages):
    story = UserStory(f"so that i can access my account as a user", "")
    result = user_story_preprocessor.check_role_means_ends_ordering(story)
    assert not result
    assert user_story_defect_types.well_formed in story.defects
    assert user_story_error_messages.bad_ordering in story.defects[user_story_defect_types.well_formed]

def test_missing_ends_correct_order(user_story_preprocessor, user_story_defect_types):
    story = UserStory(f"as a user I want to log in", "")
    result = user_story_preprocessor.check_role_means_ends_ordering(story)
    assert result
    assert user_story_defect_types.well_formed not in story.defects

def test_missing_ends_incorrect_order(user_story_preprocessor, user_story_defect_types, user_story_error_messages):
    story = UserStory(f"i want to log in as a user", "")
    result = user_story_preprocessor.check_role_means_ends_ordering(story)
    assert not result
    assert user_story_defect_types.well_formed in story.defects
    assert user_story_error_messages.bad_ordering in story.defects[user_story_defect_types.well_formed]

def test_all_indicators_missing(user_story_preprocessor, user_story_defect_types):
    story = UserStory(f"user to log in i can access my account", "")
    result = user_story_preprocessor.check_role_means_ends_ordering(story)
    assert result
    assert user_story_defect_types.well_formed not in story.defects

# check length tests
def test_story_too_long(user_story_preprocessor, user_story_defect_types, user_story_error_messages):
    story = UserStory(f"as a user I want to log in so that I can access my account and see my dashboard with all the information including my recent activities, notifications, and account settingsas a user I want to log in so that I can access my account and see my dashboard with all the information including my recent activities, notifications, and account settingsas a user I want to log in so that I can access my account and see my dashboard with all the information including my recent activities, notifications, and account settingsas a user I want to log in so that I can access my account and see my dashboard with all the information including my recent activities, notifications, and account settingsas a user I want to log in so that I can access my account and see my dashboard with all the information including my recent activities, notifications, and account settingsas a user I want to log in so that I can access my account and see my dashboard with all the information including my recent activities, notifications, and account settingsas a user I want to log in so that I can access my account and see my dashboard with all the information including my recent activities, notifications, and account settingsas a user I want to log in so that I can access my account and see my dashboard with all the information including my recent activities, notifications, and account settingsas a user I want to log in so that I can access my account and see my dashboard with all the information including my recent activities, notifications, and account settings", "")
    result = user_story_preprocessor.has_okay_length(story)
    assert not result
    assert user_story_defect_types.length in story.defects
    assert user_story_error_messages.too_long in story.defects[user_story_defect_types.length]

def test_story_max_length(user_story_preprocessor, user_story_defect_types):
    story = UserStory(f"as a user I want to log in so that I can access my account settings and dashboard as a user I want to log in so that I can access my account settings and dashboard as a user I want to log in so that I can access my", "")
    result = user_story_preprocessor.has_okay_length(story)
    assert result
    assert user_story_defect_types.length not in story.defects

# add pos to user story tests
def test_add_role_pos_to_user_story(user_story_preprocessor, pos_list, valid_story):
    story = UserStory(valid_story.lower(), valid_story)
    user_story_preprocessor.add_pos_to_user_story(story, UserStoryPart.ROLE, pos_list)
    assert story.role_pos == pos_list
    
def test_add_means_pos_to_user_story(user_story_preprocessor, pos_list, valid_story):
    story = UserStory(valid_story.lower(), valid_story)
    user_story_preprocessor.add_pos_to_user_story(story, UserStoryPart.MEANS, pos_list)
    assert story.means_pos == pos_list
    
def test_add_ends_pos_to_user_story(user_story_preprocessor, pos_list, valid_story):
    story = UserStory(valid_story.lower(), valid_story)
    user_story_preprocessor.add_pos_to_user_story(story, UserStoryPart.ENDS, pos_list)
    assert story.ends_pos == pos_list

# extract role tests
def test_extract_role(user_story_preprocessor, valid_story):
    user_story = UserStory(valid_story.lower(), valid_story)
    user_story_preprocessor.extract_role(user_story)
    assert user_story.role == "as a user,"

def test_missing_role(user_story_preprocessor, story_missing_role, user_story_defect_types, user_story_error_messages):
    user_story = UserStory(story_missing_role.lower(), story_missing_role)
    user_story_preprocessor.find_user_persona_role = Mock(return_value=None)
    user_story_preprocessor.extract_role(user_story)
    assert user_story.role is None
    assert user_story_defect_types.well_formed in user_story.defects
    assert user_story.defects[user_story_defect_types.well_formed][0] == user_story_error_messages.missing_role

# extract means tests
def test_extract_means(user_story_preprocessor, valid_story):
    user_story = UserStory(valid_story.lower(), valid_story)
    user_story_preprocessor.extract_means(user_story)
    assert user_story.means == "i want to be able to login"

def test_missing_means(user_story_preprocessor, story_missing_means, user_story_defect_types, user_story_error_messages):
    user_story = UserStory(story_missing_means.lower(), story_missing_means)
    user_story_preprocessor.extract_means(user_story)
    assert user_story.means is None
    assert user_story_defect_types.well_formed in user_story.defects
    assert user_story.defects[user_story_defect_types.well_formed][0] == user_story_error_messages.missing_means

# extract ends tests
def test_extract_ends(user_story_preprocessor, valid_story):
    user_story = UserStory(valid_story.lower(), valid_story)
    user_story_preprocessor.extract_ends(user_story)
    assert user_story.ends == "so that i can access my account."


def test_missing_ends(user_story_preprocessor, story_missing_ends, user_story_defect_types, user_story_error_messages):
    user_story = UserStory(story_missing_ends.lower(), story_missing_ends)
    user_story_preprocessor.extract_ends(user_story)
    assert user_story.ends is None
    assert user_story_defect_types.well_formed in user_story.defects
    assert user_story.defects[user_story_defect_types.well_formed][0] == user_story_error_messages.missing_ends

# remove ends tests
def test_remove_ends_basic_case(user_story_preprocessor, valid_story, story_missing_ends, ends):
    user_story = UserStory(valid_story.lower(), valid_story)
    def mock_extract_ends(story):
        return ends.lower()
    user_story_preprocessor.extract_ends = mock_extract_ends
    result = user_story_preprocessor.remove_ends(user_story)
    assert result == story_missing_ends.lower()

def test_remove_ends_no_ends_indicator(user_story_preprocessor, story_missing_ends, means):
    user_story = UserStory(story_missing_ends.lower(), story_missing_ends)
    def mock_extract_ends(story):
        return ""
    user_story_preprocessor.extract_ends = mock_extract_ends
    result = user_story_preprocessor.remove_ends(user_story)
    assert result == story_missing_ends.lower()

def test_remove_ends_empty_story(user_story_preprocessor):
    user_story = UserStory("", "")
    def mock_extract_ends(story):
        return ""
    user_story_preprocessor.extract_ends = mock_extract_ends
    result = user_story_preprocessor.remove_ends(user_story)
    assert result == ""

# find position of first noun tests
def test_find_position_of_end_of_noun_with_noun(user_story_preprocessor, pos_list, pos_text):
    user_story_preprocessor.nlp_service.is_noun = Mock(side_effect=[False, False, False, True])
    user_story_preprocessor.nlp_service.is_verb = Mock(side_effect=[False, False, True])
    result = user_story_preprocessor.find_position_of_end_of_noun(pos_list, pos_text.split())
    assert result == 4

def test_find_position_of_end_of_noun_without_noun(user_story_preprocessor, pos_list, pos_text):
    user_story_preprocessor.nlp_service.is_noun = Mock(return_value=False)
    result = user_story_preprocessor.find_position_of_end_of_noun(pos_list, pos_text.split())
    assert result == len(pos_list) + 1

def test_find_position_of_end_of_noun_empty_list(user_story_preprocessor):
    pos = []
    result = user_story_preprocessor.find_position_of_end_of_noun(pos, [])
    assert result == 1

def test_find_position_of_end_of_noun_noun_at_start(user_story_preprocessor, pos_list, pos_text):
    user_story_preprocessor.nlp_service.is_noun = Mock(side_effect=[True, False, False, False])
    user_story_preprocessor.nlp_service.is_verb = Mock(return_value=False)
    result = user_story_preprocessor.find_position_of_end_of_noun(pos_list, pos_text.split())
    assert result == 1

def test_find_position_of_end_of_noun_noun_followed_by_comma(user_story_preprocessor, pos_list, pos_text):
    user_story_preprocessor.nlp_service.is_noun = Mock(side_effect=[False, True, False, False])
    user_story_preprocessor.nlp_service.is_verb = Mock(return_value=False)
    result = user_story_preprocessor.find_position_of_end_of_noun(pos_list, pos_text.split())
    assert result == 2

# find potential means tests
def test_find_potential_means_with_means(user_story_preprocessor, valid_story, user_story_defect_types):
    story = UserStory(valid_story.lower(), valid_story)
    user_story_preprocessor.remove_ends = Mock(return_value="as a user I want to log in")
    user_story_preprocessor.nlp_service.tokenise_words = Mock(return_value=[
        ('user', 'NN'), ('I', 'PRP'), ('want', 'VB'), ('to', 'TO'),
        ('log', 'VB'), ('in', 'IN'), ('I', 'PRP'), ('can', 'MD'),
        ('access', 'VB'), ('my', 'PRP$'), ('account', 'NN')
    ])
    user_story_preprocessor.find_position_of_end_of_noun = Mock(return_value=3)
    user_story_preprocessor.remove_unnecessary_punctuation = Mock(return_value="as a user")
    user_story_preprocessor.nlp_service.has_required_number_verb_and_noun = Mock(return_value=(True, True))
    user_story_preprocessor.find_potential_means(story)
    assert story.role == "as a user"
    assert story.means == "I want to log in"
    assert story.using_potential_means
    assert user_story_defect_types.well_formed not in story.defects

def test_find_potential_means_without_valid_means(user_story_preprocessor, valid_story, user_story_defect_types, user_story_error_messages):
    story = UserStory(valid_story.lower(), valid_story)
    user_story_preprocessor.remove_ends = Mock(return_value="user i want to log in")
    user_story_preprocessor.nlp_service.tokenise_words = Mock(return_value=[
        ('user', 'NN'), ('i', 'PRP'), ('want', 'VB'), ('to', 'TO'),
        ('log', 'VB'), ('in', 'IN'), ('I', 'PRP'), ('can', 'MD')
    ])
    user_story_preprocessor.find_position_of_end_of_noun = Mock(return_value=1)
    user_story_preprocessor.remove_unnecessary_punctuation = Mock(return_value="user")
    user_story_preprocessor.nlp_service.has_required_number_verb_and_noun = Mock(return_value=(False, False))
    user_story_preprocessor.find_potential_means(story)
    assert story.role == "user i want to log in"
    assert not story.using_potential_means
    assert user_story_defect_types.well_formed in story.defects
    assert user_story_error_messages.missing_means in story.defects[user_story_defect_types.well_formed]

def test_find_potential_means_no_pos(user_story_preprocessor, valid_story, user_story_defect_types, user_story_error_messages):
    story = UserStory(valid_story.lower(), valid_story)
    user_story_preprocessor.remove_ends = Mock(return_value="as a user i want to login")
    user_story_preprocessor.nlp_service.tokenise_words = Mock(return_value=[])
    user_story_preprocessor.find_potential_means(story)
    assert story.role == None
    assert story.means == None
    assert not story.using_potential_means
    assert user_story_defect_types.well_formed in story.defects
    assert user_story_error_messages.missing_means in story.defects[user_story_defect_types.well_formed]


# find user persona role 
def test_find_user_persona_role_found(user_story_preprocessor):
    text = "As Ella, I want to login."
    user_story_preprocessor.nlp_service.tokenise_words = Mock(return_value=[('As', 'PRP'), ('Ella', 'NNP'), (',', ','), ('I', 'IN'), ('want', 'VB'), ('to', 'IN'), ('login', 'VB'), ('.', '.')])
    user_story_preprocessor.nlp_service.is_proper_noun = Mock(side_effect=lambda word: word[0] == 'Ella')
    result = user_story_preprocessor.find_user_persona_role(text)
    assert result == "As Ella"

def test_find_user_persona_role_not_found(user_story_preprocessor):
    text = "As a user, I would like to login."
    user_story_preprocessor.nlp_service.tokenise_words = Mock(return_value=[('As', 'PRP'), ('a', 'IN'), ('user', 'NN'), (',', ','), ('I', 'IN'), ('want', 'VB'), ('to', 'IN'), ('login', 'VB'), ('.', '.')])
    user_story_preprocessor.nlp_service.is_proper_noun = Mock(side_effect=lambda word: word[0] == 'Ella')
    result = user_story_preprocessor.find_user_persona_role(text)
    assert result is None

def test_find_user_persona_role_empty_text(user_story_preprocessor):
    text = ""
    user_story_preprocessor.nlp_service.tokenise_words = Mock(return_value=[])
    user_story_preprocessor.nlp_service.is_proper_noun = Mock(side_effect=lambda word: False)
    result = user_story_preprocessor.find_user_persona_role(text)
    assert result is None

# potential ends tests
def test_find_potential_ends_with_valid_ends(user_story_preprocessor):
    story = UserStory("", "")
    story.means="I want to log in so that I can access my account"
    story.means_pos = ['PRON', 'VERB', 'PART', 'VERB', 'ADP', 'PRON', 'VERB', 'DET', 'NOUN']
    
    user_story_preprocessor.nlp_service.is_noun = Mock(side_effect=[True, False, False, False, False, False, False, False])
    user_story_preprocessor.nlp_service.is_verb = Mock(side_effect=[False, True, False, True, False, False, False, False])
    
    result = user_story_preprocessor.find_potential_ends(story)
    
    assert result == "so that I can access my account"
    assert story.means == "I want to log in"

def test_find_potential_ends_no_ends_indicator(user_story_preprocessor):
    story = UserStory("", "")
    story.means="I want to log in"
    story.means_pos = ['PRON', 'VERB', 'PART', 'VERB']
    
    user_story_preprocessor.nlp_service.is_noun = Mock(side_effect=[False, False, False, False])
    user_story_preprocessor.nlp_service.is_verb = Mock(side_effect=[False, True, False, True])
    
    result = user_story_preprocessor.find_potential_ends(story)
    
    assert result is None
    assert story.means == "I want to log in"

def test_find_potential_ends_insufficient_nouns_verbs(user_story_preprocessor):
    story = UserStory("", "")
    story.means="logging in so that I can access my account"
    story.means_pos = ['VERB', 'ADP', 'PRON', 'VERB', 'DET', 'NOUN']
    
    user_story_preprocessor.nlp_service.is_noun = Mock(side_effect=[False, False, False, False, False, True])
    user_story_preprocessor.nlp_service.is_verb = Mock(side_effect=[True, False, False, True, False, False])
    
    result = user_story_preprocessor.find_potential_ends(story, min_nouns=2, min_verbs=2)
    
    assert result is None
    assert story.means == "logging in so that I can access my account"

def test_find_potential_ends_with_custom_noun_verb_counts(user_story_preprocessor):
    story = UserStory("", "")
    story.means="as a user I want to log in so that I can access my account"
    story.means_pos = ['ADP', 'DET', 'NOUN', 'PRON', 'VERB', 'PART', 'VERB', 'ADP', 'PRON', 'VERB', 'DET', 'NOUN']
    
    user_story_preprocessor.nlp_service.is_noun = Mock(side_effect=[False, False, True, False, False, False, False, False, False, False, False, True])
    user_story_preprocessor.nlp_service.is_verb = Mock(side_effect=[False, False, False, True, True, False, True])
    
    result = user_story_preprocessor.find_potential_ends(story, min_nouns=1, min_verbs=1)
    
    assert result == "so that I can access my account"
    assert story.means == "as a user I want to log in"

def test_find_potential_ends_no_verbs(user_story_preprocessor):
    story = UserStory("", "")
    story.means="access my account so that I can view my dashboard"
    story.means_pos = ['VERB', 'DET', 'NOUN', 'ADP', 'PRON', 'VERB', 'DET', 'NOUN']
    
    user_story_preprocessor.nlp_service.is_noun = Mock(side_effect=[False, False, True, False, False, False, False, True])
    user_story_preprocessor.nlp_service.is_verb = Mock(side_effect=[True, False, False, False, False, True, False, False])
    
    result = user_story_preprocessor.find_potential_ends(story, min_nouns=1, min_verbs=0)
    
    assert result == "so that I can view my dashboard"
    assert story.means == "access my account"