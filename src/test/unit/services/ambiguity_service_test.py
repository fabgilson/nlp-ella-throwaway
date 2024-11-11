import pytest

from unittest.mock import Mock
from main.services.NLPService import Ambiguity

@pytest.fixture
def ambiguity_service():
    return Ambiguity(Mock())

# comparatives and superlatives
def test_find_comparatives_superlatives_both_found(ambiguity_service):
    sentence = "The bigger, better car is the best one here."
    ambiguity_service.pos_service.tokenise_words = Mock(return_value=[('bigger', 'JJR'), ('better', 'RBR'), ('best', 'JJS')])
    comparatives, superlatives = ambiguity_service.find_comparatives_superlatives(sentence)
    
    assert comparatives == ['bigger', 'better']
    assert superlatives == ['best']

def test_find_comparatives_superlatives_only_comparatives(ambiguity_service):
    sentence = "The quicker fox jumps higher."
    ambiguity_service.pos_service.tokenise_words = Mock(return_value=[('quicker', 'JJR'), ('higher', 'RBR')])
    comparatives, superlatives = ambiguity_service.find_comparatives_superlatives(sentence)
    
    assert comparatives == ['quicker', 'higher']
    assert superlatives == []

def test_find_comparatives_superlatives_only_superlatives(ambiguity_service):
    sentence = "She is the fastest and smartest."
    ambiguity_service.pos_service.tokenise_words = Mock(return_value=[('fastest', 'JJS'), ('smartest', 'JJS')])
    comparatives, superlatives = ambiguity_service.find_comparatives_superlatives(sentence)
    
    assert comparatives == []
    assert superlatives == ['fastest', 'smartest']

def test_find_comparatives_superlatives_none_found(ambiguity_service):
    sentence = "The dog runs quickly."
    ambiguity_service.pos_service.tokenise_words = Mock(return_value=[('quickly', 'RB')])
    comparatives, superlatives = ambiguity_service.find_comparatives_superlatives(sentence)
    
    assert comparatives == []
    assert superlatives == []

def test_find_comparatives_superlatives_empty_sentence(ambiguity_service):
    sentence = ""
    ambiguity_service.pos_service.tokenise_words = Mock(return_value=[])
    comparatives, superlatives = ambiguity_service.find_comparatives_superlatives(sentence)
    
    assert comparatives == []
    assert superlatives == []

# anaphora
def test_find_anaphora_indicators_without_anaphora(ambiguity_service):
    sentence = "The book is on the table."
    ambiguity_service.pos_service.tokenise_words = Mock(return_value=[
        ('the', 'DT'), ('book', 'NN'), ('is', 'VBZ'), ('on', 'IN'), ('the', 'DT'), ('table', 'NN')
    ])
    result = ambiguity_service.find_anaphora_indicators(sentence)
    assert result == []

def test_find_anaphora_indicators_with_pronouns(ambiguity_service):
    sentence = "She gave him her book."
    ambiguity_service.pos_service.tokenise_words = Mock(return_value=[
        ('she', 'PRP'), ('gave', 'VBD'), ('him', 'PRP'), ('her', 'PRP$'), ('book', 'NN')
    ])
    result = ambiguity_service.find_anaphora_indicators(sentence)
    assert result == ['she', 'him', 'her']

def test_find_anaphora_indicators_empty_sentence(ambiguity_service):
    sentence = ""
    result = ambiguity_service.find_anaphora_indicators(sentence)
    assert result == []

def test_find_anaphora_indicators_none_sentence(ambiguity_service):
    sentence = None
    result = ambiguity_service.find_anaphora_indicators(sentence)
    assert result == []