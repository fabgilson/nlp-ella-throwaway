from flask import request

from main.services.WordlistService import WordlistService

class WordController():

    def __init__(self, word_list_service: WordlistService) -> None:
        self.word_list_service = word_list_service

    # POST /word/noun
    def add_noun_exception(self) -> list:
        """
        Takes a new noun exception, and returns the updated list of noun exceptions
        """
        word = request.get_json()['word']
        updated_exceptions = self.word_list_service.add_noun_exception(word)
        return updated_exceptions

    # POST /word/nounverb
    def add_noun_verb_exception(self) -> list:
        """
        Takes a new noun/verb exception, and returns the updated list of noun exceptions
        """
        word = request.get_json()['word']
        updated_exceptions = self.word_list_service.add_verb_noun_exception(word)
        return updated_exceptions
    
    # POST /word/verb
    def add_verb_exception(self) -> list:
        """
        Takes a new noun/verb exception, and returns the updated list of noun exceptions
        """
        word = request.get_json()['word']
        updated_exceptions = self.word_list_service.add_verb_exception(word)
        return updated_exceptions