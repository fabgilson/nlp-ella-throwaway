import pytest

from unittest.mock import Mock
from main.models.UserStory import UserStory
from main.resources.USErrorMessages import USErrorMessages
from main.resources.USErrorTypes import USErrorTypes
from main.services.userstories.UserStoryAnalyser import WellFormed

@pytest.fixture
def user_story():
    return UserStory("text", "text")

@pytest.fixture
def well_formed_analyser():
    return WellFormed(Mock(), USErrorTypes(), USErrorMessages())

@pytest.fixture
def user_story_defect_types():
    return USErrorTypes()

@pytest.fixture
def user_story_error_messages():
    return USErrorMessages()

# means starts with i tests
def test_means_starts_with_i(well_formed_analyser, user_story):
    user_story.means = "I want to login"
    starts_with_i = well_formed_analyser.check_means_starts_with_i(user_story.means)
    assert starts_with_i

def test_means_doesnt_start_with_i(well_formed_analyser, user_story):
    user_story.means = "would be good to be able to login"
    starts_with_i = well_formed_analyser.check_means_starts_with_i(user_story.means)
    assert not starts_with_i

def test_empty_means(well_formed_analyser, user_story):
    starts_with_i = well_formed_analyser.check_means_starts_with_i(user_story.means)
    assert not starts_with_i
