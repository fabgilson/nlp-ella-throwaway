import pytest

from unittest.mock import Mock
from main.models.UserStory import UserStory
from main.resources.USErrorMessages import USErrorMessages
from main.resources.USErrorTypes import USErrorTypes
from main.services.userstories.UserStoryAnalyser import Uniform

@pytest.fixture
def user_story():
    return UserStory("text", "text")

@pytest.fixture
def uniform_analyser():
    return Uniform(USErrorTypes(), USErrorMessages(), Mock())

@pytest.fixture
def user_story_defect_types():
    return USErrorTypes()

@pytest.fixture
def user_story_error_messages():
    return USErrorMessages()

# is uniform tests
def test_not_well_formatted_has_correct_defect(uniform_analyser, user_story, user_story_defect_types, user_story_error_messages):
    uniform_analyser.follows_correct_format = Mock(return_value=False)
    uniform_analyser.is_uniform(user_story)
    assert user_story_defect_types.uniform in user_story.defects
    assert user_story_error_messages.not_uniform in user_story.defects[user_story_defect_types.uniform]

def test_well_formatted_has_no_defects(uniform_analyser, user_story, user_story_defect_types):
    uniform_analyser.follows_correct_format = Mock(return_value=True)
    uniform_analyser.is_uniform(user_story)
    assert user_story_defect_types.uniform not in user_story.defects

# follows format tests
def test_follows_correct_format_with_invalid_role(uniform_analyser, user_story):
    uniform_analyser.nlp_service.get_string_without_punctuation = Mock(return_value="wrong role")
    user_story.role = "some role"
    user_story.means = "I want to do something"
    user_story.ends = "so that I can achieve something"
    user_story.original_lower_text = "as a user, I want to do something so that I can achieve something"
    result = uniform_analyser.follows_correct_format(user_story)
    assert not result

def test_follows_correct_format_with_invalid_means(uniform_analyser, user_story):
    uniform_analyser.nlp_service.get_string_without_punctuation = Mock(side_effect=lambda x: x)
    user_story.role = "as a user"
    user_story.means = "wrong means"
    user_story.ends = "so that I can achieve something"
    user_story.original_lower_text = "as a user, I want to do something so that I can achieve something"
    result = uniform_analyser.follows_correct_format(user_story)
    assert not result

def test_follows_correct_format_with_invalid_ends(uniform_analyser, user_story):
    uniform_analyser.nlp_service.get_string_without_punctuation = Mock(side_effect=lambda x: x)
    user_story.role = "as a user"
    user_story.means = "I want to do something"
    user_story.ends = "wrong ends"
    user_story.original_lower_text = "as a user, I want to do something so that I can achieve something"
    result = uniform_analyser.follows_correct_format(user_story)
    assert not result

def test_follows_correct_format_with_invalid_original_text(uniform_analyser, user_story):
    uniform_analyser.nlp_service.get_string_without_punctuation = Mock(side_effect=lambda x: x)
    user_story.role = "as a user"
    user_story.means = "I want to do something"
    user_story.ends = "so that I can achieve something"
    user_story.original_lower_text = "wrong start"
    result = uniform_analyser.follows_correct_format(user_story)
    assert not result

def test_follows_correct_format_with_valid_story(uniform_analyser, user_story):
    uniform_analyser.nlp_service.get_string_without_punctuation = Mock(side_effect=lambda x: x)
    user_story.role = "as a user"
    user_story.means = "i want to do something"
    user_story.ends = "so that I can achieve something"
    user_story.original_lower_text = "as a user, I want to do something so that I can achieve something"
    result = uniform_analyser.follows_correct_format(user_story)
    assert result
