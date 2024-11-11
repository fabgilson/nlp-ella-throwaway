from main.models.UserStory import UserStory
from main.models.AcceptanceCriteria import AcceptanceCriteria
from main.resources.AmbiguityErrorMessages import AmbiguityErrorMessages
from main.resources.AmbiguityErrorTypes import AmbiguityErrorTypes
from main.services.NLPService import NLPService
from main.services.WordlistService import WordlistService


class AmbiguityAnalyser():

    def __init__(self, nlp_servce: NLPService, word_list_service: WordlistService) -> None:
        self.nlp_service = nlp_servce
        self.word_list_service = word_list_service
        self.ambiguity_types = AmbiguityErrorTypes()
        self.ambiguity_messages = AmbiguityErrorMessages()
        self.subjectivity_analyser = Subjectivity(self.nlp_service, self.ambiguity_types, self.ambiguity_messages)
        self.vagueness_analyser = Vagueness(self.word_list_service, self.nlp_service, self.ambiguity_types, self.ambiguity_messages)
        self.non_commitment_analyser = NonCommitment(self.word_list_service, self.nlp_service, self.ambiguity_types, self.ambiguity_messages)
        self.anaphora_analyser = Anaphora(self.nlp_service, self.ambiguity_types, self.ambiguity_messages)
        self.quantifier_analyser = Quantifiers(self.word_list_service, self.nlp_service, self.ambiguity_types, self.ambiguity_messages)
        self.weakness_analyser = Weakness(self.word_list_service, self.nlp_service, self.ambiguity_types, self.ambiguity_messages)


    def is_unambiguous(self, obj: UserStory | AcceptanceCriteria):
        """
        Does all checks for ambiguity in a user story or ac
        """
        self.subjectivity_analyser.is_subjective(obj)
        self.vagueness_analyser.is_vague(obj)
        self.non_commitment_analyser.is_non_commital(obj)
        self.anaphora_analyser.has_anaphora(obj)
        self.quantifier_analyser.has_quantifiers(obj)
        self.weakness_analyser.is_weak(obj)
        return obj


class Subjectivity():

    def __init__(self, nlp_service: NLPService, ambiguity_types: AmbiguityErrorTypes, ambiguity_messages: AmbiguityErrorMessages) -> None:
        self.nlp_service = nlp_service
        self.ambiguity_types = ambiguity_types
        self.ambiguity_messages = ambiguity_messages


    def is_subjective(self, obj: UserStory | AcceptanceCriteria) -> None:
        """
        Checks that a sentence is not subjective
        """
        text_without_quotes = self.nlp_service.remove_all_quotes_from_string(obj.original_lower_text)
        comparatives, superlative = self.has_superlatives_comparatives(text_without_quotes)

        if len(superlative) > 0:
            obj.add_defect(self.ambiguity_types.ambiguity, self.ambiguity_messages.superlative(superlative))

        if len(comparatives) > 0:
            obj.add_defect(self.ambiguity_types.ambiguity, self.ambiguity_messages.comparative(comparatives))


    def has_superlatives_comparatives(self, text: str) -> tuple:
        """
        Checks for superlatives and comparatives in a sentence
        Returns a tuple of lists in the form (comparatives, superlatives)
        """
        return self.nlp_service.ambiguity_service.find_comparatives_superlatives(text)
    

class Vagueness():

    def __init__(self, word_list_service: WordlistService, nlp_service: NLPService, ambiguity_types: AmbiguityErrorTypes, ambiguity_messages: AmbiguityErrorMessages) -> None:
        self.word_list_service = word_list_service
        self.nlp_service = nlp_service
        self.ambiguity_types = ambiguity_types
        self.ambiguity_messages = ambiguity_messages


    def is_vague(self, obj: UserStory | AcceptanceCriteria) -> None:
        """
        Checks an AC or user story for vagueness and adds corresponding defects to the object
        """
        text_without_quotes = self.nlp_service.remove_all_quotes_from_string(obj.original_lower_text)
        vague_terms = self.contains_vague_terms(text_without_quotes)

        if len(vague_terms) > 0:
            obj.add_defect(self.ambiguity_types.ambiguity, self.ambiguity_messages.vague_terms(vague_terms))


    def contains_vague_terms(self, text: str) -> list:
        """
        Checks a string for whether it contains vague terms
        Returns a list of the vague terms found in the string
        """
        vague_terms = self.word_list_service.get_vague_terms_list()
        vague_terms_found = []
        for term in vague_terms:
            if f" {term} " in text:
                vague_terms_found.append(term)

        return vague_terms_found


class NonCommitment():

    def __init__(self, word_list_service: WordlistService, nlp_service: NLPService, ambiguity_types: AmbiguityErrorTypes, ambiguity_messages: AmbiguityErrorMessages) -> None:
        self.word_list_service = word_list_service
        self.nlp_service = nlp_service
        self.ambiguity_types = ambiguity_types
        self.ambiguity_messages = ambiguity_messages

    
    def is_non_commital(self, obj: UserStory | AcceptanceCriteria) -> None:
        """
        Checks for indications of non-commitment to a statement
        """
        text_without_quotes = self.nlp_service.remove_all_quotes_from_string(obj.original_lower_text)
        escape_clauses = self.contains_escape_clauses(text_without_quotes)
        
        if len(escape_clauses) > 0:
            obj.add_defect(self.ambiguity_types.ambiguity, self.ambiguity_messages.escape_clauses(escape_clauses))


    def contains_escape_clauses(self, text: str) -> list:
        """
        Checks for escape clauses in the given text
        Returns a list of found escape clauses
        """
        escape_clauses = self.word_list_service.get_escape_clause_list()
        escape_clauses_found = []
        for term in escape_clauses:
            if f" {term} " in text:
                escape_clauses_found.append(term)

        return escape_clauses_found
    

class Anaphora():

    def __init__(self, nlp_service: NLPService, ambiguity_types: AmbiguityErrorTypes, ambiguity_messages: AmbiguityErrorMessages) -> None:
        self.nlp_service = nlp_service
        self.ambiguity_types = ambiguity_types
        self.ambiguity_messages = ambiguity_messages

    
    def has_anaphora(self, obj: UserStory | AcceptanceCriteria) -> None:
        """
        Checks for indications of anaphora in a user story or AC
        Anaphora: using relative, implicit, or demonstrative pronouns/adjectives instead of explicitly referencing what is being talked about
        Example: She is running --> anaphora: who is she?
        """
        text_without_quotes = self.nlp_service.remove_all_quotes_from_string(obj.original_lower_text)
        anaphora = self.contains_anaphora_indicators(text_without_quotes)

        if len(anaphora) > 0:
            obj.add_defect(self.ambiguity_types.ambiguity, self.ambiguity_messages.anaphora(anaphora))


    def contains_anaphora_indicators(self, text: str) -> list:
        """
        Checks for instances of anaphora in the given text
        Returns a list of found anaphora indicators
        """
        return self.nlp_service.ambiguity_service.find_anaphora_indicators(text)
    
class Quantifiers():

    def __init__(self, word_list_service: WordlistService, nlp_service: NLPService, ambiguity_types: AmbiguityErrorTypes, ambiguity_messages: AmbiguityErrorMessages) -> None:
        self.word_list_service = word_list_service
        self.nlp_service = nlp_service
        self.ambiguity_types = ambiguity_types
        self.ambiguity_messages = ambiguity_messages

    
    def has_quantifiers(self, obj: UserStory | AcceptanceCriteria) -> None:
        """
        Checks for quantifiers in a user story or AC
        """
        text_without_quotes = self.nlp_service.remove_all_quotes_from_string(obj.original_lower_text)
        quantifiers = self.contains_quantifiers(text_without_quotes)

        if len(quantifiers) > 0:
            obj.add_defect(self.ambiguity_types.ambiguity, self.ambiguity_messages.quantifiers(quantifiers))


    def contains_quantifiers(self, text: str) -> list:
        """
        Checks for instances of quantification in the given text
        Returns a list of found quantification indicators
        """
        quantifiers = self.word_list_service.get_quantifiers_list()
        quantifiers_found = []
        for term in quantifiers:
            if f" {term} " in text:
                quantifiers_found.append(term)

        return quantifiers_found
    

class Weakness():

    def __init__(self, word_list_service: WordlistService, nlp_service: NLPService, ambiguity_types: AmbiguityErrorTypes, ambiguity_messages: AmbiguityErrorMessages) -> None:
        self.word_list_service = word_list_service
        self.nlp_service = nlp_service
        self.ambiguity_types = ambiguity_types
        self.ambiguity_messages = ambiguity_messages

    
    def is_weak(self, obj: UserStory | AcceptanceCriteria) -> None:
        """
        Checks for weakness in a user story or AC
        """
        text_without_quotes = self.nlp_service.remove_all_quotes_from_string(obj.original_lower_text)
        weak_verbs = self.contains_weak_verbs(text_without_quotes)

        if len(weak_verbs) > 0:
            obj.add_defect(self.ambiguity_types.ambiguity, self.ambiguity_messages.weakness(weak_verbs))


    def contains_weak_verbs(self, text: str) -> list:
        """
        Checks for instances of weak verbs in the given text
        Returns a list of found weak verbs
        """
        weak_verbs = self.word_list_service.get_weak_verbs_list()
        tokens = self.nlp_service.tokenise_words(text)
        weak_verbs_found = []
        for token in tokens:
            word = token[0]
            if (self.nlp_service.is_verb(token) or self.nlp_service.is_modal(token)) and word in weak_verbs:
                weak_verbs_found.append(word)

        return weak_verbs_found