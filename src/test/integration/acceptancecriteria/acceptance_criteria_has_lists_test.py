import pytest
import os

from unittest.mock import Mock

from main.repositories.NounExceptionRepository import NounExceptionRepository
from main.repositories.VagueTermsRepository import VagueTermsRepository
from main.repositories.QuantifiersRespository import QuantifiersRepository
from main.repositories.VerbExceptionRepository import VerbExceptionRepository
from main.repositories.VerbNounExceptionRepository import VerbNounExceptionRepository
from main.repositories.EscapeClauseRepository import EscapeClauseRepository
from main.repositories.WeakVerbsRepository import WeakVerbsRepository
from main.resources.USErrorMessages import USErrorMessages
from main.resources.USErrorTypes import USErrorTypes
from main.services.NLPService import NLPService
from main.services.acceptancecriteria.AcceptanceCriteriaAnalyser import Singular
from main.services.WordlistService import WordlistService

@pytest.fixture
def int_singular_analyser():
    base_path = os.path.dirname(os.path.realpath(__file__))
    noun_repo = NounExceptionRepository(base_path)
    verb_noun_repo = VerbNounExceptionRepository(base_path)
    verb_repo = VerbExceptionRepository(base_path)
    vague_terms_repo = VagueTermsRepository(base_path)
    escape_repo = EscapeClauseRepository(base_path)
    quantifier_repo = QuantifiersRepository(base_path)
    weak_verbs_repository = WeakVerbsRepository(base_path)
    word_lists = WordlistService(verb_noun_repo, noun_repo, verb_repo, vague_terms_repo, escape_repo, quantifier_repo, weak_verbs_repository)
    nlp_service = NLPService(word_lists)
    return Singular(nlp_service, USErrorTypes(), USErrorMessages())

@pytest.mark.parametrize("ac", [
    "Given I am on the registration form, and I enter valid values for my first name and last name, email address, type the same password twice, and optionally a date of birth, ",
    "Given I am on the registration form, and I enter invalid values (i.e. an empty first name, an empty last name without checking the “I have no surname” checkbox, non-alphabetical characters except hyphen, space or apostrophe for either first or last name), ",
    "Given I am on the registration form, and I enter a first name or last name that is more than 64 characters, ",
    "Given I am on the registration form, and I enter an empty or malformed[1] email address (i.e. an email address that does not have a prefix, second-level domain, and top-level domain or has invalid characters), ",
    "Given I am on the registration form, and I enter a weak password (i.e. is less than 8 characters, does not contain at least one lower case letter, one upper case letter, one number, and one special character), ",
    "Given I am on the login form, and I enter a malformed (i.e. an email address that does not have a prefix, second-level domain, and top-level domain or has invalid characters) or empty email address, ",
    "Given I am on the login form, and I enter an empty password or the wrong password for the corresponding email address, "
])
def test_ac_with_list_is_identified(int_singular_analyser, ac):
    result = int_singular_analyser.nlp_service.check_for_lists(ac)
    assert result


@pytest.mark.parametrize("ac", [
    "when I click the check box marked “I have no surname” ticked, ",
    "when I click the “Sign up” button, ",
    "when I see the home page, ",
    "when I click the “Not registered? Create an account” link, ",
    "then I am automatically logged in to my new account, and I see my user profile page."
    "then an error message tells me “{First/Last} name cannot be empty and must only include letters, spaces, hyphens or apostrophes”, and no account is created."
    "then an error message tells me “{First/Last} name must be 64 characters long or less ”",
    "then an error message tells me “Your password must be at least 8 characters long and include at least one uppercase letter, one lowercase letter, one number, and one special character.”",
    "then an error message tells me “The email address is unknown, or the password is invalid”."
])
def test_acs_with_no_list_are_not_flagged(int_singular_analyser, ac):
    result = int_singular_analyser.nlp_service.check_for_lists(ac)
    assert not result