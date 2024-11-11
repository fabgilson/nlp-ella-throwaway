import pytest

from unittest.mock import Mock
from main.services.NLPService import Punctuation

@pytest.fixture
def punctuation_service():
    return Punctuation()

# remove punctuation
def test_get_string_without_punctuation_only_punctuation(punctuation_service):
    input_text = ".,!?;:"
    expected_output = ""
    result = punctuation_service.get_string_without_punctuation(input_text)
    assert result == expected_output

def test_get_string_without_punctuation_mixed_text(punctuation_service):
    input_text = "Hello, World! This is a test."
    expected_output = "Hello World This is a test"
    result = punctuation_service.get_string_without_punctuation(input_text)
    assert result == expected_output

def test_get_string_without_punctuation_no_punctuation(punctuation_service):
    input_text = "Hello World This is a test"
    expected_output = "Hello World This is a test"
    result = punctuation_service.get_string_without_punctuation(input_text)
    assert result == expected_output

def test_get_string_without_punctuation_numbers_and_punctuation(punctuation_service):
    input_text = "Test123, check456. Let's remove 789!"
    expected_output = "Test check Lets remove "
    result = punctuation_service.get_string_without_punctuation(input_text)
    assert result == expected_output

def test_get_string_without_punctuation_special_characters(punctuation_service):
    input_text = "@#Hello$%^&*()World+=_{}[]"
    expected_output = "HelloWorld"
    result = punctuation_service.get_string_without_punctuation(input_text)
    assert result == expected_output

def test_get_string_without_punctuation_empty_string(punctuation_service):
    input_text = ""
    expected_output = ""
    result = punctuation_service.get_string_without_punctuation(input_text)
    assert result == expected_output

# remove quotes
def test_remove_quotes_from_sentence_no_quotes_returns_original_text(punctuation_service):
    text = "There are no quotes in this text"
    assert punctuation_service.remove_all_quotes_from_string(text) == text

def test_remove_quotes_from_sentence_quotes_returns_text_without_curly_double_quotes(punctuation_service):
    text = "There are “quotes” in this text"
    expected = "There are in this text"
    assert punctuation_service.remove_all_quotes_from_string(text) == expected

def test_remove_quotes_from_sentence_quotes_returns_text_without_double_quotes(punctuation_service):
    text = "There are \"quotes\" in this text"
    expected = "There are in this text"
    assert punctuation_service.remove_all_quotes_from_string(text) == expected

def test_remove_quotes_from_sentence_quotes_returns_text_without_curly_single_quotes(punctuation_service):
    text = "There are ‘quotes’ in this text"
    expected = "There are in this text"
    assert punctuation_service.remove_all_quotes_from_string(text) == expected

def test_remove_quotes_from_sentence_quotes_returns_text_without_single_quotes(punctuation_service):
    text = "There are 'quotes' in this text"
    expected = "There are in this text"
    assert punctuation_service.remove_all_quotes_from_string(text) == expected

def test_remove_quotes_from_sentence_quotes_has_apostrophe_is_ignored(punctuation_service):
    text = "Sentences that have apostrophe's are ignored"
    expected = "Sentences that have apostrophe's are ignored"
    assert punctuation_service.remove_all_quotes_from_string(text) == expected

# splitting on separating punctuation tests
def test_split_on_single_punctuation(punctuation_service):
    chunk = "As a user I want to be able to login so that I can access my account. I also want to edit my account."
    expected = ["As a user I want to be able to login so that I can access my account", "I also want to edit my account."]
    assert punctuation_service.split_on_punctuation(chunk) == expected

def test_split_on_end_punctuation(punctuation_service):
    chunk = "As a user I want to be able to login so that I can access my account."
    expected = ["As a user I want to be able to login so that I can access my account."]
    assert punctuation_service.split_on_punctuation(chunk) == expected

def test_multiple_separating_punctuation(punctuation_service):
    chunk = "As a user I want to be able to login; edit details; view accounts."
    expected = ["As a user I want to be able to login", "edit details", "view accounts."]
    assert punctuation_service.split_on_punctuation(chunk) == expected

def test_text_contains_examples_ignored(punctuation_service):
    chunk = "As a user I want to be able to login and do things e.g. edit details and view accounts."
    expected = ["As a user I want to be able to login and do things  edit details and view accounts."]
    assert punctuation_service.split_on_punctuation(chunk) == expected

def test_text_contains_titles_ignored(punctuation_service):
    chunk = "as dr. bill i want to be able to login and do things edit details and view accounts."
    expected = ["as  bill i want to be able to login and do things edit details and view accounts."]
    assert punctuation_service.split_on_punctuation(chunk) == expected

# check punctuation has text either side
def test_punctuation_no_follow_text_is_fine(punctuation_service):
    punctuation_service.split_on_punctuation = Mock(return_value=["text"])
    assert not punctuation_service.has_separating_punctuation_with_following_text("")

def test_punctuation_follow_text_is_not_fine(punctuation_service):
    punctuation_service.split_on_punctuation = Mock(return_value=["text ", "text"])
    assert punctuation_service.has_separating_punctuation_with_following_text("")