import re

from main.models.UserStory import UserStory
from main.resources.USErrorMessages import USErrorMessages
from main.resources.USErrorTypes import USErrorTypes
from main.services.WordlistService import WordlistService
from main.services.NLPService import NLPService

ROLE_INDICATOR_USING_PERSONAS = "as"
MEANS_INDICATOR = "i want"
ENDS_INDICATOR = "so that"

class UserStoryAnalyser():

    def __init__(self, nlp_servce: NLPService, word_list_service: WordlistService) -> None:
        self.nlp_service = nlp_servce
        self.word_list_service = word_list_service
        self.user_story_defect_types = USErrorTypes()
        self.user_story_error_messages = USErrorMessages()
        self.well_formed_analyser = WellFormed(self.nlp_service, self.user_story_defect_types, self.user_story_error_messages)
        self.minimal_analyser = Minimal(self.word_list_service, self.user_story_defect_types, self.user_story_error_messages, self.nlp_service)
        self.full_sentence_analyser = FullSentence(self.nlp_service, self.user_story_defect_types, self.user_story_error_messages)
        self.atomic_analyser = Atomic(self.full_sentence_analyser, self.word_list_service, self.nlp_service, self.user_story_defect_types, self.user_story_error_messages)
        self.uniform_analyser = Uniform(self.user_story_defect_types, self.user_story_error_messages, self.nlp_service)


    def analyse_user_story(self, story: UserStory) -> UserStory:
        """
        Analyse a user story using the quality criteria
        """
        self.well_formed_analyser.is_well_formed(story)
        self.atomic_analyser.is_atomic(story)
        self.minimal_analyser.is_minimal(story)
        self.full_sentence_analyser.is_full_sentence(story)
        self.uniform_analyser.is_uniform(story)
        return story
    

class WellFormed():

    def __init__(self, nlp_service: NLPService, user_story_defect_types: USErrorTypes, user_story_error_messages: USErrorMessages) -> None:
        self.user_story_defect_types = user_story_defect_types
        self.user_story_error_messages = user_story_error_messages
        self.nlp_service = nlp_service


    def is_well_formed(self, story: UserStory) -> None:
        """
        Check that a user story is well-formed
        """
        self.check_means(story)
        

    def check_means(self, story: UserStory) -> None:
        """
        Check that the means of a story passes all associated rules
        """
        not_well_formed_but_has_means = self.user_story_defect_types.well_formed in story.defects \
            and self.user_story_error_messages.missing_means not in story.defects[self.user_story_defect_types.well_formed]
        well_formed = self.user_story_defect_types.well_formed not in story.defects

        starts_with_i = self.check_means_starts_with_i(story.means)

        if not starts_with_i and (not_well_formed_but_has_means or well_formed):
            story.add_defect(self.user_story_defect_types.well_formed, self.user_story_error_messages.means_doesnt_start_with_i)

    
    def check_means_starts_with_i(self, means: str) -> bool:
        """
        Checks that the first word of the means is "I"
        Mostly needed in the case of using a potential means
        """
        if means:
            word_list = means.split()
            if word_list[0].lower() == "i":
                return True
        return False
    

class FullSentence():

    def __init__(self, nlp_service: NLPService, user_story_defect_types: USErrorTypes, user_story_error_messages: USErrorMessages) -> None:
        self.user_story_defect_types = user_story_defect_types
        self.user_story_error_messages = user_story_error_messages
        self.nlp_service = nlp_service


    def is_full_sentence(self, story: UserStory) -> None:
        """
        Checks that a story is a full sentence
        """
        self.check_means(story)
        self.check_role(story)
        self.check_ends(story)
    

    def check_means(self, story: UserStory) -> None:
        """
        Check the means has the correct parts of speech
        """
        not_well_formed_but_has_means = self.user_story_defect_types.well_formed in story.defects \
            and self.user_story_error_messages.missing_means not in story.defects[self.user_story_defect_types.well_formed]
        well_formed = self.user_story_defect_types.well_formed not in story.defects

        missing_verb, missing_noun = self.check_means_pos(story.means_pos)

        if missing_verb and (not_well_formed_but_has_means or well_formed):
            story.add_defect(self.user_story_defect_types.full_sentence, self.user_story_error_messages.means_missing_second_verb)    
        if missing_noun and (not_well_formed_but_has_means or well_formed):
            story.add_defect(self.user_story_defect_types.full_sentence, self.user_story_error_messages.means_missing_noun)

    
    def check_means_pos(self, pos: list, min_verbs: int = 2, min_nouns: int = 1) -> bool:
        """
        Check that the means contains at least one verb and one noun
        """
        found_verbs, found_noun = self.nlp_service.has_required_number_verb_and_noun(pos, min_nouns, min_verbs, True)
        missing_verb = pos != None and not found_verbs
        missing_noun = pos != None and not found_noun
        return missing_verb, missing_noun
    

    def check_role(self, story: UserStory) -> None:
        """
        Given a role, check it is passing all associated rules
        """
        missing_noun = self.check_role_missing_noun(story.role_pos)

        not_well_formed_and_missing_role = self.user_story_defect_types.well_formed in story.defects \
            and self.user_story_error_messages.missing_role not in story.defects[self.user_story_defect_types.well_formed]
        well_formed = self.user_story_defect_types.well_formed not in story.defects

        if missing_noun and (not_well_formed_and_missing_role or well_formed):
            story.add_defect(self.user_story_defect_types.full_sentence, self.user_story_error_messages.role_doesnt_end_with_noun)


    def check_role_missing_noun(self, pos: list) -> bool:
        """
        Check that a role has a noun in the final position (actor)
        If it doesn't, return false
        """
        if pos:
            last_word = pos[-1]
            if self.nlp_service.is_noun(last_word, True):
                return False
        return True
    

    def check_ends(self, story: UserStory) -> None:
        """
        Checks that the ends has some words after the indicator
        """
        ends = story.ends
        if ends != None and len(ends.split()) < 3:
            story.add_defect(self.user_story_defect_types.full_sentence, self.user_story_error_messages.ends_missing_words)


class Atomic():

    def __init__(self, full_sentence_analyser: FullSentence, word_list_service: WordlistService, nlp_service: NLPService, \
                 user_story_defect_types: USErrorTypes, user_story_error_messages: USErrorMessages) -> None:
        self.user_story_defect_types = user_story_defect_types
        self.user_story_error_messages = user_story_error_messages
        self.word_list_service = word_list_service
        self.nlp_service = nlp_service
        self.full_sentence_analyser = full_sentence_analyser


    def is_atomic(self, story: UserStory) -> None:
        """
        Check that a user story is atomic
        """
        more_than_one_role = self.has_conjunctions_with_valid_chunks_either_side(story.role, self.valid_role)
        more_than_one_means = self.has_conjunctions_with_valid_chunks_either_side(story.means, self.valid_means)
        list_of_verbs_in_means = self.nlp_service.list_service.has_list_of_verbs(story.means)

        if more_than_one_role:
            story.add_defect(self.user_story_defect_types.atomic, self.user_story_error_messages.more_than_one_role)

        if more_than_one_means:
            story.add_defect(self.user_story_defect_types.atomic, self.user_story_error_messages.more_than_one_means)

        if list_of_verbs_in_means:
            story.add_defect(self.user_story_defect_types.atomic, self.user_story_error_messages.list_of_verbs_in_means)


    def has_conjunctions_with_valid_chunks_either_side(self, chunk: str, is_valid) -> bool:
        """
        Check if a chunk of a user story has conjunctions
        For it to be a violation, it needs to be a valid chunk either side of the conjunction
        If it does, add a defect to say it violates atomicity
        """
        parts = self.split_string_on_conjunctions(chunk)
        num_valid = 0

        for part in parts:
            if part not in self.word_list_service.conjunctions:
                pos = self.nlp_service.tokenise_words(part)
                valid = is_valid(pos)
                if valid:
                    num_valid += 1

        if num_valid > 1:
            return True
        return False

    
    def valid_means(self, means_pos):
        """
        Check if a section of a means is valid
        """
        num_verbs_required_in_each_part = 1
        missing_noun, missing_verb = self.full_sentence_analyser.check_means_pos(means_pos, num_verbs_required_in_each_part)
        return not missing_noun and not missing_verb
    

    def valid_role(self, role_pos):
        """
        Check if a section of a role is valid
        """
        missing_noun = self.full_sentence_analyser.check_role_missing_noun(role_pos)
        return not missing_noun


    def split_string_on_conjunctions(self, chunk: str) -> list:
        """
        Split a string on each conjunction, removing the conjuction and leaving the text either side of it
        """
        if chunk:
            pattern = r'(?<!\w)(?:' + '|'.join(map(re.escape, self.word_list_service.conjunctions)) + r')(?!\w)'
            split_text = re.split(pattern, chunk)
            split_text = [part.strip() for part in split_text if part.strip()]
            return split_text
        return []
    

class Minimal():

    def __init__(self, word_list_service: WordlistService, user_story_defect_types: USErrorTypes, user_story_error_messages: USErrorMessages, nlp_service: NLPService) -> None:
        self.user_story_defect_types = user_story_defect_types
        self.user_story_error_messages = user_story_error_messages
        self.word_list_service = word_list_service
        self.nlp_service = nlp_service

    
    def is_minimal(self, story: UserStory) -> None:
        """
        Checks if a user story is minimal
        Adds appropriate defects to violations list if it is not
        """
        has_separating_punctuation = self.has_separating_punctuation_with_following_text(story.original_lower_text)
        
        if has_separating_punctuation:
            story.add_defect(self.user_story_defect_types.minimal, self.user_story_error_messages.has_separating_punctuation)

        has_brackets_containing_information = self.has_brackets_containing_information(story.original_lower_text)

        if has_brackets_containing_information:
            story.add_defect(self.user_story_defect_types.minimal, self.user_story_error_messages.has_brackets)


    def has_separating_punctuation_with_following_text(self, story_text: str) -> bool:
        """
        Checks if there is separating punctuation in the user story with text following it
        True if there is, otherwise false
        """
        return self.nlp_service.has_separating_punctuation_with_following_text(story_text)
    

    def has_brackets_containing_information(self, text: str) -> bool:
        """
        Check a piece of text for brackets
        Returns true if there are *any* sets of well formed brackets containing text
        Otherwise false
        """
        return len(self.nlp_service.has_brackets_containing_information(text)) > 0

    
class Uniform():

    def __init__(self, user_story_defect_types: USErrorTypes, user_story_error_messages: USErrorMessages, nlp_service: NLPService) -> None:
        self.user_story_defect_types = user_story_defect_types
        self.user_story_error_messages = user_story_error_messages
        self.nlp_service = nlp_service

    
    def is_uniform(self, story: UserStory) -> None:
        """
        Controls checks for if a user story is uniform
        """
        well_formatted = self.follows_correct_format(story)

        if not well_formatted:
            story.add_defect(self.user_story_defect_types.uniform, self.user_story_error_messages.not_uniform)


    def follows_correct_format(self, story: UserStory) -> bool:
        """
        Checks whether a user story follows the expected format:
        - Role with 'as'
        - Means starts with 'I want'
        - Ends starts with 'so that'
        - There is no text in the original text before 'as'
        """

        if story.role and not self.nlp_service.get_string_without_punctuation(story.role).startswith(ROLE_INDICATOR_USING_PERSONAS):
            return False

        if story.means and not self.nlp_service.get_string_without_punctuation(story.means).startswith(MEANS_INDICATOR):
            return False
        
        if story.ends and not self.nlp_service.get_string_without_punctuation(story.ends).startswith(ENDS_INDICATOR):
            return False
        
        if story.role and not self.nlp_service.get_string_without_punctuation(story.original_lower_text).startswith(ROLE_INDICATOR_USING_PERSONAS):
            return False
        
        return True

        
                
