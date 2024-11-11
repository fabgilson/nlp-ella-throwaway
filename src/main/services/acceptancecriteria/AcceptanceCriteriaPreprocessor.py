from main.models.AcceptanceCriteria import AcceptanceCriteria
from main.resources.ACErrorMessages import ACErrorMessages
from main.resources.ACErrorTypes import ACErrorTypes
from main.resources.USErrorMessages import USErrorMessages
from main.resources.USErrorTypes import USErrorTypes
from main.services.NLPService import NLPService

CONTEXT_INDICATOR = "given"
EVENT_INDICATOR = "when"
OUTCOME_INDICATOR = "then"
AND_INDICATOR = " and "
MAX_LENGTH = 70

class AcceptanceCriteriaPreprocessor():

    def __init__(self, nlp_service: NLPService) -> None:
        self.acceptance_criteria_defect_types = ACErrorTypes()
        self.acceptance_criteria_error_messages = ACErrorMessages()
        self.nlp_service = nlp_service


    def pre_process_ac_text(self, ac: str = None) -> AcceptanceCriteria:
        """
        Preprocess the acceptance criteria:
            - make it lowercase
            - check the order of the given-when-then clauses
            - check there are not multiple of any indicators
            - split the ac into the clauses
        """
        ac_number = ac[1]
        ac_text = ac[0]
        acceptance_criteria = AcceptanceCriteria(ac_text.lower(), ac_text)
        acceptance_criteria.ac_number = ac_number
        in_order = self.check_context_event_outcome_ordering(acceptance_criteria)
        max_one_of_each_indicator = self.check_only_one_context_event_outcome(acceptance_criteria)
        can_be_processed = in_order and max_one_of_each_indicator
        if not can_be_processed:
            return acceptance_criteria, can_be_processed
        self.split_story_into_chunks(acceptance_criteria)
        self.tokenise_and_pos_tag_chunks(acceptance_criteria)
        self.add_and_clauses_to_ac(acceptance_criteria)
        return acceptance_criteria, can_be_processed
    

    def check_only_one_context_event_outcome(self, ac: AcceptanceCriteria) -> bool:
        """
        Checks that there is only one role, one event, and one outcome
        If there is more than one of any, an atomic violation is added
        """
        text = self.nlp_service.remove_all_quotes_from_string(ac.original_lower_text)
        text = self.remove_brackets(text)
        max_one_context = text.count(CONTEXT_INDICATOR) <= 1
        max_one_event = text.count(EVENT_INDICATOR) <= 1
        max_one_outcome = text.count(OUTCOME_INDICATOR) <= 1
        
        if not max_one_context:
            ac.add_defect(self.acceptance_criteria_defect_types.essentiality, self.acceptance_criteria_error_messages.more_than_one_context)
        if not max_one_event:
            ac.add_defect(self.acceptance_criteria_defect_types.essentiality, self.acceptance_criteria_error_messages.more_than_one_event)
        if not max_one_outcome:
            ac.add_defect(self.acceptance_criteria_defect_types.essentiality, self.acceptance_criteria_error_messages.more_than_one_outcome)

        return max_one_event and max_one_outcome and max_one_context


    def check_context_event_outcome_ordering(self, ac: AcceptanceCriteria) -> bool:
        """
        Checks the ordering of the context, event, outcome
        Returns true if it is in the correct order (context -> event -> outcome) otherwise false
        """
        text = self.nlp_service.remove_all_quotes_from_string(ac.original_lower_text)
        text = self.remove_brackets(text)
        context_position = text.find(CONTEXT_INDICATOR)
        event_position = text.find(EVENT_INDICATOR)
        outcome_position = text.find(OUTCOME_INDICATOR)

        context_before_event = context_position == -1 or event_position == -1 or context_position < event_position
        context_before_outcome = context_position == -1 or outcome_position == -1 or context_position < outcome_position
        event_before_outcome = event_position == -1 or outcome_position == -1 or event_position < outcome_position
        all_indicators_missing = context_position == -1 and event_position == -1 and outcome_position == -1

        correct_ordering = (context_before_event and event_before_outcome and context_before_outcome) or all_indicators_missing

        if not correct_ordering:
            ac.add_defect(self.acceptance_criteria_defect_types.integrous, self.acceptance_criteria_error_messages.out_of_order)

        return correct_ordering
    

    def split_story_into_chunks(self, ac: AcceptanceCriteria) -> None:
        """
        Split acs into chunks to get the context, event, and outcome.
        """
        self.extract_context(ac)
        self.extract_event(ac)
        self.extract_outcome(ac) 

    
    def extract_context(self, ac: AcceptanceCriteria) -> None:
        """
        Extract the context from the original ac text.
        If there is no context, add it to the list of defects.
        """
        context_position = ac.original_lower_text.find(CONTEXT_INDICATOR)
        event_position = ac.original_lower_text.find(EVENT_INDICATOR)
        outcome_position = ac.original_lower_text.find(OUTCOME_INDICATOR)
        context = None

        if context_position != -1 and event_position != -1:
            context = ac.original_lower_text[context_position:event_position]
        elif context_position !=-1 and event_position == -1 and outcome_position != -1:
            context = ac.original_lower_text[context_position:outcome_position]
        elif context_position !=-1 and event_position == -1 and outcome_position == -1:
            context = ac.original_lower_text[context_position:]
        else:
            ac.add_defect(self.acceptance_criteria_defect_types.integrous, self.acceptance_criteria_error_messages.missing_context)
        
        ac.context = context.lower().strip() if context else None


    def extract_event(self, ac: AcceptanceCriteria) -> None:
        """
        Extract the event from the original ac text.
        If there is no event, add it to the list of defects.
        """
        event_position = ac.original_lower_text.find(EVENT_INDICATOR)
        outcome_position = ac.original_lower_text.find(OUTCOME_INDICATOR)
        event = None

        if event_position != -1:
            if outcome_position != -1:
                event = ac.original_lower_text[event_position:outcome_position]
            else:
                event = ac.original_lower_text[event_position:]
        else:
            ac.add_defect(self.acceptance_criteria_defect_types.integrous, self.acceptance_criteria_error_messages.missing_event)

        ac.event = event.lower().strip() if event else None

    
    def extract_outcome(self, ac: AcceptanceCriteria) -> None:
        """
        Extract the outcome from the original ac text.
        If there is no outcome, add it to the list of defects.
        """
        outcome_position = ac.original_lower_text.find(OUTCOME_INDICATOR)
        outcome = None

        if outcome_position != -1:
            outcome = ac.original_lower_text[outcome_position:]
        else:
            ac.add_defect(self.acceptance_criteria_defect_types.integrous, self.acceptance_criteria_error_messages.missing_outcome)

        ac.outcome = outcome.lower().strip() if outcome else None

    
    def tokenise_and_pos_tag_chunks(self, ac: AcceptanceCriteria) -> None:
        """
        Splits the chunks of an AC into tokens and tag each token with a POS tag
        """
        ac.context_pos = self.tokenise_and_pos_tag_chunk(ac.context)
        ac.event_pos = self.tokenise_and_pos_tag_chunk(ac.event)
        ac.outcome_pos = self.tokenise_and_pos_tag_chunk(ac.outcome)


    def tokenise_and_pos_tag_chunk(self, chunk: str | None) -> None:
        """
        Take the role of an AC and split it into tokens and tag each token with a POS tag
        """
        if chunk != None:
            return self.nlp_service.tokenise_words(self.nlp_service.get_string_without_punctuation(chunk))
        return None
    

    def add_and_clauses_to_ac(self, ac: AcceptanceCriteria) -> None:
        """
        Adds and clauses to the AC for all parts
        """
        ac.context_and_clauses = self.extract_and_clauses(ac.context)
        ac.event_and_clauses = self.extract_and_clauses(ac.event)
        ac.outcome_and_clauses = self.extract_and_clauses(ac.outcome)
    

    def extract_and_clauses(self, chunk: str | None) -> list:
        """
        Extract all AND clauses from the AC and return a list of them
        """
        and_clauses = []
        if chunk != None:
            parts = chunk.split(AND_INDICATOR)
            prev_part = (parts[0], False)
            for part in parts:
                part_tokens = self.tokenise_and_pos_tag_chunk(part)
                verbs, nouns = self.nlp_service.has_required_number_verb_and_noun(part_tokens, 1, 1)
                is_clause = True if verbs and nouns else False
                if is_clause:
                    if not prev_part[1] and prev_part[0] != part:
                        full_clause = f"{prev_part[0]} and {part}"
                        and_clauses.append(full_clause)
                    else:
                        and_clauses.append(part)
                    prev_part = (part, True)
                else:
                    if len(and_clauses) > 0:
                        full_clause = f"{and_clauses[-1]} and {part}"
                        and_clauses[-1] = full_clause
                    else:
                        and_clauses.append(part)
                    prev_part = (part, False)
            return and_clauses
        else:
            return []
        

    def remove_brackets(self, text: str | None) -> str:
        """
        Remove all brackets from the text, for when checking if there are more than one of an indicator
        """
        text_in_brackets = self.nlp_service.has_brackets_containing_information(text)
        for item in text_in_brackets:
            text = text.replace(item, "")
        return text


