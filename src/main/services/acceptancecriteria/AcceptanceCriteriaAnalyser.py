import re
from collections import defaultdict

from main.models.AcceptanceCriteria import AcceptanceCriteria
from main.resources.ACErrorMessages import ACErrorMessages
from main.resources.ACErrorTypes import ACErrorTypes
from main.services.WordlistService import WordlistService
from main.services.NLPService import NLPService

AND_INDICATOR = " and "
AND_CLAUSE_THRESHOLD = 10

class AcceptanceCriteriaAnalyser():

    def __init__(self, nlp_service: NLPService, word_list_service: WordlistService) -> None:
        self.nlp_service = nlp_service
        self.word_list_service = word_list_service
        self.acceptance_criteria_defect_types = ACErrorTypes()
        self.acceptance_criteria_error_messages = ACErrorMessages()
        self.integrous_analyser = Integrous(self.nlp_service, self.acceptance_criteria_defect_types, self.acceptance_criteria_error_messages)
        self.essential_analyser = Essential(self.nlp_service, self.acceptance_criteria_defect_types, self.acceptance_criteria_error_messages, self.word_list_service)
        self.singular_analyser = Singular(self.nlp_service, self.acceptance_criteria_defect_types, self.acceptance_criteria_error_messages)
        self.unique_analyser = Unique(self.nlp_service, self.acceptance_criteria_defect_types, self.acceptance_criteria_error_messages)


    def analyse_acceptance_criteria(self, acceptance_criteria: AcceptanceCriteria) -> AcceptanceCriteria:
        """
        Analyse a user story using the quality criteria
        """
        self.integrous_analyser.is_integrous(acceptance_criteria)
        self.essential_analyser.is_essential(acceptance_criteria)
        self.singular_analyser.is_singular(acceptance_criteria)
        return acceptance_criteria
    

class Integrous():

    def __init__(self, nlp_service: NLPService, acceptance_criteria_defect_types: ACErrorTypes, acceptance_criteria_error_messages: ACErrorMessages) -> None:
        self.nlp_service = nlp_service
        self.acceptance_criteria_defect_types = acceptance_criteria_defect_types
        self.acceptance_criteria_error_messages = acceptance_criteria_error_messages


    def is_integrous(self, ac: AcceptanceCriteria) -> None:
        """
        Checks if an AC is integrous
        - All chunks need to have 1 noun and 1 verb each
        """
        context_verbs, context_nouns = self.nlp_service.has_required_number_verb_and_noun(ac.context_pos, 1, 2) # two required verbs because 'given' is considered a verb
        event_verbs, event_nouns = self.nlp_service.has_required_number_verb_and_noun(ac.event_pos, 1, 1)
        outcome_verbs, outcome_nouns = self.nlp_service.has_required_number_verb_and_noun(ac.outcome_pos, 1, 1)

        if ac.context != None and not (context_verbs and context_nouns):
            ac.add_defect(self.acceptance_criteria_defect_types.integrous, self.acceptance_criteria_error_messages.context_missing_noun_or_verb)
        if ac.event != None and not (event_verbs and event_nouns):
            ac.add_defect(self.acceptance_criteria_defect_types.integrous, self.acceptance_criteria_error_messages.event_missing_noun_or_verb)
        if ac.outcome != None and not (outcome_verbs and outcome_nouns):
            ac.add_defect(self.acceptance_criteria_defect_types.integrous, self.acceptance_criteria_error_messages.outcome_missing_noun_or_verb)
    

class Essential():

    def __init__(self, nlp_service: NLPService, acceptance_criteria_defect_types: ACErrorTypes, acceptance_criteria_error_messages: ACErrorMessages, word_list_service: WordlistService) -> None:
        self.nlp_service = nlp_service
        self.word_list_service = word_list_service
        self.acceptance_criteria_defect_types = acceptance_criteria_defect_types
        self.acceptance_criteria_error_messages = acceptance_criteria_error_messages

    
    def is_essential(self, ac: AcceptanceCriteria) -> None:
        """
        Checks that an AC is essential
        - Does not have separating punctuation that indicates more than one sentence
        - Does not have extra information inside brackets (only a defect if the brackets contain information)
        """
        text_without_quotes = self.nlp_service.remove_all_quotes_from_string(ac.original_lower_text)
        has_separating_punctuation = self.nlp_service.has_separating_punctuation_with_following_text(text_without_quotes)
        
        if has_separating_punctuation:
            ac.add_defect(self.acceptance_criteria_defect_types.essentiality, self.acceptance_criteria_error_messages.separating_punctuation)

        information_in_brackets = self.nlp_service.has_brackets_containing_information(text_without_quotes)

        if len(information_in_brackets) > 0:
            ac.add_defect(self.acceptance_criteria_defect_types.essentiality, self.acceptance_criteria_error_messages.info_in_brackets)
    

class Singular():

    def __init__(self, nlp_service: NLPService, acceptance_criteria_defect_types: ACErrorTypes, acceptance_criteria_error_messages: ACErrorMessages) -> None:
        self.acceptance_criteria_defect_types = acceptance_criteria_defect_types
        self.acceptance_criteria_error_messages = acceptance_criteria_error_messages
        self.nlp_service = nlp_service


    def is_singular(self, ac: AcceptanceCriteria) -> None:
        """
        Checks that an AC is singular
        - Does not have more AND clauses in a chunk than the given threshold (defined as constant in this file)
        """
        context_has_lists = (any(self.nlp_service.check_for_lists(part) for part in ac.context_and_clauses) or 
                             self.nlp_service.list_service.has_list_of_verbs(ac.context))
        event_has_lists = (any(self.nlp_service.check_for_lists(part) for part in ac.event_and_clauses) or 
                           self.nlp_service.list_service.has_list_of_verbs(ac.event))
        outcome_has_lists = (any(self.nlp_service.check_for_lists(part) for part in ac.outcome_and_clauses) or 
                             self.nlp_service.list_service.has_list_of_verbs(ac.outcome))

        if event_has_lists or context_has_lists or outcome_has_lists:
            ac.add_defect(self.acceptance_criteria_defect_types.singularity, self.acceptance_criteria_error_messages.list_in_ac)
    

class Unique(): 

    def __init__(self, nlp_service: NLPService, acceptance_criteria_defect_types: ACErrorTypes, acceptance_criteria_error_messages: ACErrorMessages) -> None:
        self.nlp_service = nlp_service
        self.acceptance_criteria_defect_types = acceptance_criteria_defect_types
        self.acceptance_criteria_error_messages = acceptance_criteria_error_messages

    
    def are_unique(self, acs: list) -> None:
        """
        Checks for both full and semantic duplicates
        """
        acs_text_only = list(map(lambda ac: ac.original_lower_text, acs))
        full_duplicates = self.has_full_duplicates(acs_text_only)

        uniqueness_defects = []
        
        for item in full_duplicates.items():
            duplicate_indices = item[1]
            error = self.acceptance_criteria_error_messages.full_duplicates(duplicate_indices)
            uniqueness_defects.append(error)

        return uniqueness_defects
    
    
    def has_full_duplicates(self, acs: list):
        """
        Gets a dictionary of any full duplicates (exact matches) in the set of ACs
        Returns a dictionary of the AC text mapping to a list of indices that have that AC
        """
        indices_dict = defaultdict(list)

        for index, ac in enumerate(acs):
            indices_dict[ac].append(index)

        duplicates_dict = {string: indices for string, indices in indices_dict.items() if len(indices) > 1}

        return duplicates_dict

