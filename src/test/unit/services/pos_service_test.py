import pytest

from unittest.mock import Mock
from main.services.NLPService import POS

@pytest.fixture
def pos_service():
    return POS(Mock())

# potential noun or verb tests
def test_is_not_noun_or_verb_but_in_list(pos_service):
    pos_service.wordlist_service.get_verb_noun_exceptions = Mock(return_value=['test'])
    pos_service.is_noun = Mock(return_value=False)
    pos_service.is_verb = Mock(return_value=False)
    assert not pos_service.is_potential_noun_or_verb(['test'])

def test_is_not_in_list_but_is_noun(pos_service):
    pos_service.wordlist_service.get_verb_noun_exceptions = Mock(return_value=['test'])
    pos_service.is_noun = Mock(return_value=True)
    pos_service.is_verb = Mock(return_value=False)
    assert not pos_service.is_potential_noun_or_verb(['testing'])

def test_is_not_in_list_but_is_verb(pos_service):
    pos_service.wordlist_service.get_verb_noun_exceptions = Mock(return_value=['test'])
    pos_service.is_noun = Mock(return_value=False)
    pos_service.is_verb = Mock(return_value=True)
    assert not pos_service.is_potential_noun_or_verb(['testing'])

def test_is_not_in_list_but_is_verb_and_noun(pos_service):
    pos_service.wordlist_service.get_verb_noun_exceptions = Mock(return_value=['test'])
    pos_service.is_noun = Mock(return_value=True)
    pos_service.is_verb = Mock(return_value=True)
    assert not pos_service.is_potential_noun_or_verb(['testing'])

def test_is_not_in_list_and_is_not_verb_or_noun(pos_service):
    pos_service.wordlist_service.get_verb_noun_exceptions = Mock(return_value=['test'])
    pos_service.is_noun = Mock(return_value=False)
    pos_service.is_verb = Mock(return_value=False)
    assert not pos_service.is_potential_noun_or_verb(['testing'])

def test_is_in_list_and_is_verb(pos_service):
    pos_service.wordlist_service.get_verb_noun_exceptions = Mock(return_value=['test'])
    pos_service.is_noun = Mock(return_value=False)
    pos_service.is_verb = Mock(return_value=True)
    assert pos_service.is_potential_noun_or_verb(['test'])

def test_is_in_list_and_is_noun(pos_service):
    pos_service.wordlist_service.get_verb_noun_exceptions = Mock(return_value=['test'])
    pos_service.is_noun = Mock(return_value=True)
    pos_service.is_verb = Mock(return_value=False)
    assert pos_service.is_potential_noun_or_verb(['test'])

def test_is_in_list_and_is_noun_and_verb(pos_service):
    pos_service.wordlist_service.get_verb_noun_exceptions = Mock(return_value=['test'])
    pos_service.is_noun = Mock(return_value=True)
    pos_service.is_verb = Mock(return_value=True)
    assert pos_service.is_potential_noun_or_verb(['test'])

# is noun tests
def test_is_noun_true(pos_service):
    token = ('dog', 'NN')
    pos_service.noun = ['NN', 'NNS']
    pos_service.wordlist_service.get_noun_exceptions = Mock(return_value=['cat'])
    result = pos_service.is_noun(token, True)
    assert result

def test_is_noun_false_due_to_pos_tag(pos_service):
    token = ('run', 'VB')
    pos_service.noun = ['NN', 'NNS']
    pos_service.wordlist_service.get_noun_exceptions = Mock(return_value=['cat'])
    pos_service.wordlist_service.get_verb_exceptions = Mock(return_value=['dog'])
    result = pos_service.is_noun(token, True)
    assert not result

def test_is_noun_false_due_to_exception(pos_service):
    token = ('cat', 'NN')
    pos_service.noun = ['NN', 'NNS']
    pos_service.wordlist_service.get_noun_exceptions = Mock(return_value=['cat'])
    pos_service.wordlist_service.get_verb_exceptions = Mock(return_value=['dog'])
    result = pos_service.is_noun(token, True)
    assert not result

def test_is_noun_true_with_plural_noun(pos_service):
    token = ('dogs', 'NNS')
    pos_service.noun = ['NN', 'NNS']
    pos_service.wordlist_service.get_noun_exceptions = Mock(return_value=['cat'])
    result = pos_service.is_noun(token, True)
    assert result

def test_is_noun_empty_token(pos_service):
    token = ('', '')
    pos_service.noun = ['NN', 'NNS']
    pos_service.wordlist_service.get_noun_exceptions = Mock(return_value=['cat'])
    pos_service.wordlist_service.get_verb_exceptions = Mock(return_value=['dog'])
    result = pos_service.is_noun(token, True)
    assert not result

def test_is_noun_empty_exceptions(pos_service):
    token = ('dog', 'NN')
    pos_service.noun = ['NN', 'NNS']
    pos_service.wordlist_service.get_noun_exceptions = Mock(return_value=[])
    result = pos_service.is_noun(token, True)
    assert result

# is verb tests
def test_is_verb_true(pos_service):
    token = ('dog', 'VB')
    pos_service.verb = ['VB', 'VBP']
    pos_service.wordlist_service.get_verb_exceptions = Mock(return_value=['cat'])
    result = pos_service.is_verb(token)
    assert result

def test_is_verb_false_due_to_pos_tag(pos_service):
    token = ('run', 'NN')
    pos_service.verb = ['VB', 'VBP']
    pos_service.wordlist_service.get_verb_exceptions = Mock(return_value=['cat'])
    result = pos_service.is_verb(token)
    assert not result

def test_is_verb_false_due_to_exception(pos_service):
    token = ('cat', 'VB')
    pos_service.verb = ['VB', 'VBP']
    pos_service.wordlist_service.get_verb_exceptions = Mock(return_value=['cat'])
    result = pos_service.is_verb(token)
    assert not result

def test_is_verb_empty_token(pos_service):
    token = ('', '')
    pos_service.verb = ['VB', 'VBP']
    pos_service.wordlist_service.get_verb_exceptions = Mock(return_value=['cat'])
    result = pos_service.is_verb(token)
    assert not result

# tests for extract noun phrases
def test_extract_noun_phrases_simple(pos_service):
    pos_service.noun_phrase_grammar = "NP: {<DT>?<JJ>*<NN.*>+}"
    text = "The quick brown fox"
    pos_service.extract_noun_phrases = Mock(return_value=["quick brown fox"])
    result = pos_service.extract_noun_phrases(text)
    assert result == ["quick brown fox"]

def test_extract_noun_phrases_multiple(pos_service):
    pos_service.noun_phrase_grammar = "NP: {<DT>?<JJ>*<NN.*>+}"
    text = "The quick brown fox jumps over the lazy dog"
    pos_service.extract_noun_phrases = Mock(return_value=["quick brown fox", "lazy dog"])
    result = pos_service.extract_noun_phrases(text)
    assert result == ["quick brown fox", "lazy dog"]

def test_extract_noun_phrases_no_noun_phrases(pos_service):
    pos_service.noun_phrase_grammar = "NP: {<DT>?<JJ>*<NN.*>+}"
    text = "He jumps over"
    pos_service.extract_noun_phrases = Mock(return_value=[])
    result = pos_service.extract_noun_phrases(text)
    assert result == []

# tests for has required number of verbs and nouns
def test_has_required_number_verb_and_noun_sufficient(pos_service):
    pos_service.is_noun = Mock(side_effect=[True, False])
    pos_service.is_verb = Mock(return_value=True)
    pos = [('dog', 'NN'), ('run', 'VB')]
    result = pos_service.has_required_number_verb_and_noun(pos, 1, 1)
    assert result == (True, True)

def test_has_required_number_verb_and_noun_insufficient_nouns(pos_service):
    pos_service.is_noun = Mock(return_value=False)
    pos_service.is_verb = Mock(return_value=True)
    pos_service.get_potential_verbs_nouns = Mock(return_value=(True, False))
    pos = [('run', 'VB')]
    result = pos_service.has_required_number_verb_and_noun(pos, 1, 1)
    assert result == (True, False)

def test_has_required_number_verb_and_noun_insufficient_verbs(pos_service):
    pos_service.is_noun = Mock(return_value=True)
    pos_service.is_verb = Mock(return_value=False)
    pos_service.get_potential_verbs_nouns = Mock(return_value=(False, True))
    pos = [('dog', 'NN')]
    result = pos_service.has_required_number_verb_and_noun(pos, 1, 1)
    assert result == (False, True)

def test_has_required_number_verb_and_noun_empty_pos(pos_service):
    pos_service.is_noun = Mock(return_value=True)
    pos_service.is_verb = Mock(return_value=True)
    pos_service.get_potential_verbs_nouns = Mock(return_value=(False, False))
    pos = []
    result = pos_service.has_required_number_verb_and_noun(pos, 1, 1)
    assert result == (False, False)

def test_has_required_number_verb_and_noun_ignore_i_as_noun(pos_service):
    pos_service.is_noun = Mock(return_value=False)
    pos_service.is_verb = Mock(return_value=True)
    pos_service.get_potential_verbs_nouns = Mock(return_value=(True, False))
    pos = [('I', 'NN'), ('run', 'VB')]
    result = pos_service.has_required_number_verb_and_noun(pos, 1, 1, True)
    assert result == (True, False)

def test_has_required_number_verb_and_noun_insufficient_nouns_but_found_potential_noun(pos_service):
    pos_service.is_noun = Mock(return_value=False)
    pos_service.is_verb = Mock(return_value=True)
    pos_service.get_potential_verbs_nouns = Mock(return_value=(True, True))
    pos = [('I', 'VB'), ('run', 'VB')]
    result = pos_service.has_required_number_verb_and_noun(pos, 1, 1, True)
    assert result == (True, True)

def test_has_required_number_verb_and_noun_insufficient_verbs_but_found_potential_verb(pos_service):
    pos_service.is_noun = Mock(return_value=True)
    pos_service.is_verb = Mock(return_value=False)
    pos_service.get_potential_verbs_nouns = Mock(return_value=(True, True))
    pos = [('I', 'NN'), ('run', 'NN')]
    result = pos_service.has_required_number_verb_and_noun(pos, 1, 1, True)
    assert result == (True, True)

def test_has_required_number_verb_and_noun_insufficient_nouns_and_not_found_potential_noun(pos_service):
    pos_service.is_noun = Mock(return_value=False)
    pos_service.is_verb = Mock(return_value=True)
    pos_service.get_potential_verbs_nouns = Mock(return_value=(True, False))
    pos = [('I', 'VB'), ('run', 'VB')]
    result = pos_service.has_required_number_verb_and_noun(pos, 1, 1, True)
    assert result == (True, False)

def test_has_required_number_verb_and_noun_insufficient_verbs_and_not_found_potential_verb(pos_service):
    pos_service.is_noun = Mock(return_value=True)
    pos_service.is_verb = Mock(return_value=False)
    pos_service.get_potential_verbs_nouns = Mock(return_value=(False, True))
    pos = [('I', 'NN'), ('run', 'NN')]
    result = pos_service.has_required_number_verb_and_noun(pos, 1, 1, True)
    assert result == (False, True)

# tests for get potential verbs and nouns
def test_get_potential_verbs_nouns_potential(pos_service):
    pos_service.check_potential_verbs_or_nouns = Mock(return_value=True)
    result = pos_service.get_potential_verbs_nouns(False, True, ['run'], ['dog'], 1, 1)
    assert result == (True, True)

def test_get_potential_verbs_nouns_no_potential(pos_service):
    pos_service.check_potential_verbs_or_nouns = Mock(return_value=False)
    result = pos_service.get_potential_verbs_nouns(False, False, [], ['dog'], 1, 1)
    assert result == (False, False)

# tests for check potential verbs or nouns
def test_check_potential_verbs_or_nouns_sufficient_potential(pos_service):
    pos_service.is_potential_noun_or_verb = Mock(side_effect=[True, False])
    result = pos_service.check_potential_verbs_or_nouns(['run'], ['dog'], 1, 0)
    assert result == True

def test_check_potential_verbs_or_nouns_insufficient_potential(pos_service):
    pos_service.is_potential_noun_or_verb = Mock(side_effect=[False, False])
    result = pos_service.check_potential_verbs_or_nouns(['run'], [], 1, 0)
    assert result == False

def test_check_potential_verbs_or_nouns_no_missing(pos_service):
    pos_service.is_potential_noun_or_verb = Mock(side_effect=[False])
    result = pos_service.check_potential_verbs_or_nouns(['run'], ['dog'], 0, 1)
    assert result == True
