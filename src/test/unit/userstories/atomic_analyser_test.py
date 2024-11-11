import pytest

from unittest.mock import Mock
from main.models.UserStory import UserStory
from main.resources.USErrorMessages import USErrorMessages
from main.resources.USErrorTypes import USErrorTypes
from main.services.userstories.UserStoryAnalyser import Atomic

@pytest.fixture
def user_story():
    return UserStory("text", "text")

@pytest.fixture
def atomic_analyser():
    return Atomic(Mock(), Mock(), Mock(), USErrorTypes(), USErrorMessages())

@pytest.fixture
def user_story_defect_types():
    return USErrorTypes()

@pytest.fixture
def user_story_error_messages():
    return USErrorMessages()

# is atomic tests
def test_more_than_one_role_reports_defect(atomic_analyser, user_story, user_story_defect_types, user_story_error_messages):
    atomic_analyser.has_conjunctions_with_valid_chunks_either_side = Mock(side_effect=[True, False])
    atomic_analyser.nlp_service.list_service.has_list_of_verbs = Mock(return_value=False)
    atomic_analyser.is_atomic(user_story)
    assert user_story_defect_types.atomic in user_story.defects
    assert user_story_error_messages.more_than_one_role in user_story.defects[user_story_defect_types.atomic]
    assert len(user_story.defects[user_story_defect_types.atomic]) == 1

def test_more_than_one_means_reports_defect(atomic_analyser, user_story, user_story_defect_types, user_story_error_messages):
    atomic_analyser.has_conjunctions_with_valid_chunks_either_side = Mock(side_effect=[False, True])
    atomic_analyser.nlp_service.list_service.has_list_of_verbs = Mock(return_value=False)
    atomic_analyser.is_atomic(user_story)
    assert user_story_defect_types.atomic in user_story.defects
    assert user_story_error_messages.more_than_one_means in user_story.defects[user_story_defect_types.atomic]
    assert len(user_story.defects[user_story_defect_types.atomic]) == 1

def test_more_than_one_means_and_role_reports_defect(atomic_analyser, user_story, user_story_defect_types, user_story_error_messages):
    atomic_analyser.has_conjunctions_with_valid_chunks_either_side = Mock(side_effect=[True, True])
    atomic_analyser.nlp_service.list_service.has_list_of_verbs = Mock(return_value=False)
    atomic_analyser.is_atomic(user_story)
    assert user_story_defect_types.atomic in user_story.defects
    assert user_story_error_messages.more_than_one_role in user_story.defects[user_story_defect_types.atomic]
    assert user_story_error_messages.more_than_one_means in user_story.defects[user_story_defect_types.atomic]
    assert len(user_story.defects[user_story_defect_types.atomic]) == 2

# conjunction checker tests
def test_no_parts(atomic_analyser):
    atomic_analyser.split_string_on_conjunctions = Mock(return_value=[])
    atomic_analyser.word_list_service.conjunctions = ["and", "or", "&", "+", "/", "<", ">"]
    def mock_is_valid(pos):
        return True
    assert not atomic_analyser.has_conjunctions_with_valid_chunks_either_side("", mock_is_valid)

def test_one_valid_parts(atomic_analyser):
    atomic_analyser.split_string_on_conjunctions = Mock(return_value=["One part"])
    atomic_analyser.word_list_service.conjunctions = ["and", "or", "&", "+", "/", "<", ">"]
    def mock_is_valid(pos):
        return True
    assert not atomic_analyser.has_conjunctions_with_valid_chunks_either_side("", mock_is_valid)

def test_two_valid_parts(atomic_analyser):
    atomic_analyser.split_string_on_conjunctions = Mock(return_value=["One part", "two parts"])
    atomic_analyser.word_list_service.conjunctions = ["and", "or", "&", "+", "/", "<", ">"]
    def mock_is_valid(pos):
        return True
    assert atomic_analyser.has_conjunctions_with_valid_chunks_either_side("", mock_is_valid)

def test_one_invalid_part(atomic_analyser):
    atomic_analyser.split_string_on_conjunctions = Mock(return_value=["One part"])
    atomic_analyser.word_list_service.conjunctions = ["and", "or", "&", "+", "/", "<", ">"]
    def mock_is_valid(pos):
        return False
    assert not atomic_analyser.has_conjunctions_with_valid_chunks_either_side("", mock_is_valid)

def test_two_invalid_part(atomic_analyser):
    atomic_analyser.split_string_on_conjunctions = Mock(return_value=["One part", "two parts"])
    atomic_analyser.word_list_service.conjunctions = ["and", "or", "&", "+", "/", "<", ">"]
    def mock_is_valid(pos):
        return False
    assert not atomic_analyser.has_conjunctions_with_valid_chunks_either_side("", mock_is_valid)

# valid means tests
def test_valid_means_both_present(atomic_analyser):
    atomic_analyser.full_sentence_analyser.check_means_pos = Mock(return_value=(False, False))
    assert atomic_analyser.valid_means(["Noun", "Verb"])

def test_valid_means_missing_noun(atomic_analyser):
    atomic_analyser.full_sentence_analyser.check_means_pos = Mock(return_value=(True, False))
    assert not atomic_analyser.valid_means(["", "Verb"])

def test_valid_means_missing_verb(atomic_analyser):
    atomic_analyser.full_sentence_analyser.check_means_pos = Mock(return_value=(False, True))
    assert not atomic_analyser.valid_means(["Noun", ""])
    
def test_valid_means_missing_both(atomic_analyser):
    atomic_analyser.full_sentence_analyser.check_means_pos = Mock(return_value=(True, True))
    assert not atomic_analyser.valid_means(["", ""])

# valid role tests
def test_valid_role_noun_present(atomic_analyser):
    atomic_analyser.full_sentence_analyser.check_role_missing_noun = Mock(return_value=False)
    assert atomic_analyser.valid_role(["Noun"])

def test_valid_role_noun_missing(atomic_analyser):
    atomic_analyser.full_sentence_analyser.check_role_missing_noun = Mock(return_value=True)
    assert not atomic_analyser.valid_role([""])

# splitting on conjunctions tests
def test_split_on_single_conjunction(atomic_analyser):
    chunk = "I like apples and oranges"
    expected = ["I like apples", "oranges"]
    atomic_analyser.word_list_service.conjunctions = ["and", "or", "&", "+", "/", "<", ">"]
    assert atomic_analyser.split_string_on_conjunctions(chunk) == expected

def test_split_on_multiple_conjunctions(atomic_analyser):
    chunk = "I like apples, and oranges, + I don't like bananas"
    expected = ["I like apples,", "oranges,", "I don't like bananas"]
    atomic_analyser.word_list_service.conjunctions = ["and", "or", "&", "+", "/", "<", ">"]
    assert atomic_analyser.split_string_on_conjunctions(chunk) == expected

def test_no_conjunctions(atomic_analyser):
    chunk = "I like apples oranges bananas"
    expected = ["I like apples oranges bananas"]
    atomic_analyser.word_list_service.conjunctions = ["and", "or", "&", "+", "/", "<", ">"]
    assert atomic_analyser.split_string_on_conjunctions(chunk) == expected

def test_empty_string(atomic_analyser):
    chunk = ""
    expected = []
    atomic_analyser.word_list_service.conjunctions = ["and", "or", "&", "+", "/", "<", ">"]
    assert atomic_analyser.split_string_on_conjunctions(chunk) == expected

def test_conjunctions_with_extra_spaces(atomic_analyser):
    chunk = "I like apples &   oranges and  I don't like bananas"
    expected = ["I like apples", "oranges", "I don't like bananas"]
    atomic_analyser.word_list_service.conjunctions = ["and", "or", "&", "+", "/", "<", ">"]
    assert atomic_analyser.split_string_on_conjunctions(chunk) == expected

def test_conjunctions_at_edges(atomic_analyser):
    chunk = "+ I like apples or oranges and"
    expected = ["I like apples", "oranges"]
    atomic_analyser.word_list_service.conjunctions = ["and", "or", "&", "+", "/", "<", ">"]
    assert atomic_analyser.split_string_on_conjunctions(chunk) == expected

def test_split_with_punctuation(atomic_analyser):
    chunk = "I like apples / oranges and I don't like bananas."
    expected = ["I like apples", "oranges", "I don't like bananas."]
    atomic_analyser.word_list_service.conjunctions = ["and", "or", "&", "+", "/", "<", ">"]
    assert atomic_analyser.split_string_on_conjunctions(chunk) == expected

def test_mixed_case_conjunctions(atomic_analyser):
    chunk = "I like apples + oranges / I don't like bananas"
    expected = ["I like apples", "oranges", "I don't like bananas"]
    atomic_analyser.word_list_service.conjunctions = ["and", "or", "&", "+", "/", "<", ">"]
    assert atomic_analyser.split_string_on_conjunctions(chunk) == expected
