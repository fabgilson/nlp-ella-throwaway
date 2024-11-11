from main.repositories.EscapeClauseRepository import EscapeClauseRepository
from main.repositories.NounExceptionRepository import NounExceptionRepository
from main.repositories.QuantifiersRespository import QuantifiersRepository
from main.repositories.VagueTermsRepository import VagueTermsRepository
from main.repositories.VerbExceptionRepository import VerbExceptionRepository
from main.repositories.VerbNounExceptionRepository import VerbNounExceptionRepository
from main.repositories.WeakVerbsRepository import WeakVerbsRepository

class WordlistService():

    def __init__(self, 
                verb_noun_exceptions_repository: VerbNounExceptionRepository, 
                noun_exception_repository: NounExceptionRepository, 
                verb_exception_repository: VerbExceptionRepository,
                vague_terms_repository: VagueTermsRepository,
                escape_clause_repository: EscapeClauseRepository,
                quantifiers_repository: QuantifiersRepository,
                weak_verbs_repository: WeakVerbsRepository
            ) -> None:
        self.conjunctions = ["and", "or", "&", "+", "/", "<", ">"]
        self.verb_noun_exception_repository = verb_noun_exceptions_repository
        self.noun_exception_repository = noun_exception_repository
        self.verb_exception_repository = verb_exception_repository
        self.vague_terms_repository = vague_terms_repository
        self.escape_clause_repository = escape_clause_repository
        self.quantifiers_repository = quantifiers_repository
        self.weak_verbs_repository = weak_verbs_repository


    def get_noun_exceptions(self) -> list:
        """
        Returns a list of noun exceptions from the repository
        """
        return self.noun_exception_repository.get_noun_exceptions()
    

    def get_verb_exceptions(self) -> list:
        """
        Returns a list of verb exceptions from the repository
        """
        return self.verb_exception_repository.get_verb_exceptions()
    

    def get_verb_noun_exceptions(self) -> list:
        """
        Returns a list of verb/noun exceptions from the repository
        """
        return self.verb_noun_exception_repository.get_verb_noun_exceptions()
    

    def add_noun_exception(self, word: str) -> list:
        """
        Adds a new noun exception to the respository
        These are words that should not be considered nouns in any case
        Returns the updated list of nouns
        """
        self.noun_exception_repository.add_noun_exception(word)
        return self.noun_exception_repository.get_noun_exceptions()
    

    def add_verb_exception(self, word: str) -> list:
        """
        Adds a new noun exception to the respository
        These are words that should not be considered nouns in any case
        Returns the updated list of nouns
        """
        self.verb_exception_repository.add_verb_exception(word)
        return self.verb_exception_repository.get_verb_exceptions()
    

    def add_verb_noun_exception(self, word: str) -> list:
        """
        Adds a new word to the verb/noun exception list in the repository
        These words are any domain specific words that could be considered either a noun or verb
        Returns the updated list of verb/noun exceptions
        """
        self.verb_noun_exception_repository.add_verb_noun_exception(word)
        return self.verb_noun_exception_repository.get_verb_noun_exceptions()
    

    def get_vague_terms_list(self) -> list:
        """
        Gets a list of vague terms from the repository
        Returns a python list of those words
        """
        return self.vague_terms_repository.get_vague_terms()
    
    def get_escape_clause_list(self) -> list:
        """
        Gets a list of escape clauses from the repository
        Returns a python list of those words/phrases
        """
        return self.escape_clause_repository.get_escape_clauses()
    
    def get_quantifiers_list(self) -> list:
        """
        Gets a list of escape clauses from the repository
        Returns a python list of those words/phrases
        """
        return self.quantifiers_repository.get_quantifiers()
    
    def get_weak_verbs_list(self) -> list:
        """
        Gets a list of weak verbs from the repository
        Returns a python list of those verbs
        """
        return self.weak_verbs_repository.get_weak_verbs()