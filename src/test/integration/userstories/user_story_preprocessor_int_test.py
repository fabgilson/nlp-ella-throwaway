import os
import pytest

from main.models.UserStory import UserStory
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
from main.services.WordlistService import WordlistService
from main.services.userstories.UserStoryPreprocessor import UserStoryPreprocessor

@pytest.fixture
def user_story_defect_types():
    return USErrorTypes()

@pytest.fixture
def user_story_error_messages():
    return USErrorMessages()

@pytest.fixture
def user_story_preprocessor():
    base_path = str(os.path.dirname(os.path.realpath(__file__)))
    base_path = base_path.replace("/test/integration/userstories", "")

    # register repositories
    verb_noun_exception_repository = VerbNounExceptionRepository(base_path)
    noun_exception_repository = NounExceptionRepository(base_path)
    verb_exception_repository = VerbExceptionRepository(base_path)
    vague_terms_repository = VagueTermsRepository(base_path)
    escape_clause_repository = EscapeClauseRepository(base_path)
    quantifiers_repository = QuantifiersRepository(base_path)
    weak_verbs_repository = WeakVerbsRepository(base_path)

    # register services
    word_list_service = WordlistService(
        verb_noun_exception_repository, 
        noun_exception_repository, 
        verb_exception_repository, 
        vague_terms_repository,
        escape_clause_repository,
        quantifiers_repository,
        weak_verbs_repository
    )
    nlp_service = NLPService(word_list_service)

    return UserStoryPreprocessor(nlp_service)


# separating punctuation
@pytest.mark.parametrize(
    "story_text, role, means, ends", 
    [
        (
            "as a data publishing user, be able to import data in Excel, so that i do not have to convert data formats in order to use the data packager.",
            "as a data publishing user,",
            "be able to import data in excel,",
            "so that i do not have to convert data formats in order to use the data packager."
        ),
        (
            "as a data-consuming user, have consistent use of colour on map visualisations, so that i can better understand the visual logic of the map view.",
            "as a data-consuming user,",
            "have consistent use of colour on map visualisations,",
            "so that i can better understand the visual logic of the map view."
        ),
        (
            "as a data publishing user, be able to import data from Fiscal Data Package descriptor file, so that i do not have to convert data formats in order to use the data packager.",
            "as a data publishing user,",
            "be able to import data from fiscal data package descriptor file,",
            "so that i do not have to convert data formats in order to use the data packager."
        ),
        (
            "As a user, I would like to login to my account so that I can access my account.",
            "as a user,",
            "i would like to login to my account",
            "so that i can access my account."
        )
    ]
)
def test_means_missing_i_want_has_correct_means_identified(user_story_preprocessor, story_text, role, means, ends):
    story = UserStory(story_text.lower(), story_text)
    user_story_preprocessor.split_story_into_chunks(story)
    assert story.role == role
    assert story.means == means
    assert story.ends == ends