import pytest

from unittest.mock import Mock
from main.models.UserStory import UserStory
from main.resources.USErrorMessages import USErrorMessages
from main.resources.USErrorTypes import USErrorTypes
from main.services.userstories.UserStoryAnalyser import Minimal

@pytest.fixture
def user_story():
    return UserStory("text", "text")

@pytest.fixture
def minimal_analyser():
    return Minimal(Mock(), USErrorTypes(), USErrorMessages(), Mock())

@pytest.fixture
def user_story_defect_types():
    return USErrorTypes()

@pytest.fixture
def user_story_error_messages():
    return USErrorMessages()

# is minimal tests
def test_is_minimal_no_violations(minimal_analyser, user_story, user_story_defect_types):
    minimal_analyser.nlp_service.has_separating_punctuation_with_following_text = Mock(return_value=False)
    minimal_analyser.nlp_service.has_brackets_containing_information = Mock(return_value=[])    
    minimal_analyser.is_minimal(user_story)
    assert user_story_defect_types.minimal not in user_story.defects

def test_is_minimal_separating_punctuation_violation(minimal_analyser, user_story, user_story_defect_types, user_story_error_messages):
    minimal_analyser.nlp_service.has_separating_punctuation_with_following_text = Mock(return_value=True)
    minimal_analyser.nlp_service.has_brackets_containing_information = Mock(return_value=[])    
    minimal_analyser.is_minimal(user_story)
    assert user_story_defect_types.minimal in user_story.defects
    assert len(user_story.defects[user_story_defect_types.minimal]) == 1
    assert user_story_error_messages.has_separating_punctuation in user_story.defects[user_story_defect_types.minimal]

def test_is_minimal_brackets_violation(minimal_analyser, user_story, user_story_defect_types, user_story_error_messages):
    minimal_analyser.nlp_service.has_separating_punctuation_with_following_text = Mock(return_value=False)
    minimal_analyser.nlp_service.has_brackets_containing_information = Mock(return_value=["True"])    
    minimal_analyser.is_minimal(user_story)
    assert user_story_defect_types.minimal in user_story.defects
    assert len(user_story.defects[user_story_defect_types.minimal]) == 1
    assert user_story_error_messages.has_brackets in user_story.defects[user_story_defect_types.minimal]

def test_is_minimal_both_violations(minimal_analyser, user_story, user_story_defect_types, user_story_error_messages):
    minimal_analyser.nlp_service.has_separating_punctuation_with_following_text = Mock(return_value=True)
    minimal_analyser.nlp_service.has_brackets_containing_information = Mock(return_value=["True"])    
    minimal_analyser.is_minimal(user_story)
    assert user_story_defect_types.minimal in user_story.defects
    assert len(user_story.defects[user_story_defect_types.minimal]) == 2
    assert user_story_error_messages.has_brackets in user_story.defects[user_story_defect_types.minimal]
    assert user_story_error_messages.has_separating_punctuation in user_story.defects[user_story_defect_types.minimal]