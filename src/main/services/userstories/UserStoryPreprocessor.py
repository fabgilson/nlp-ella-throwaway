from main.models.UserStory import UserStory
from main.resources.USErrorMessages import USErrorMessages
from main.resources.USErrorTypes import USErrorTypes
from main.types.UserStoryParts import UserStoryPart
from main.services.NLPService import NLPService

ROLE_INDICATOR = "as a"
ROLE_INDICATOR_USING_PERSONAS = "as"
MEANS_INDICATOR = "i want"
ENDS_INDICATOR = "so that"
POTENTIAL_ENDS_INDICATOR = "so"
MAX_LENGTH = 70

class UserStoryPreprocessor():

    def __init__(self, nlp_service: NLPService) -> None:
        self.user_story_defect_types = USErrorTypes()
        self.user_story_error_messages = USErrorMessages(MAX_LENGTH)
        self.nlp_service = nlp_service


    def pre_process_story_text(self, story_text: str = None) -> UserStory:
        """
        Preprocess the story text:
            - make it lowercase
            - check there is only one role, one means, one ends -> if not don't keep processing
            - check that the ordering of role, means, ends is correct -> if not don't keep processing
            - create user story object
            - use POS tagger to tag all tokens with a part of speech
        """
        user_story = UserStory(story_text.lower(), story_text)
        right_number_of_roles_means_ends = self.check_only_one_role_means_ends(user_story)
        correct_ordering_of_role_means_ends = self.check_role_means_ends_ordering(user_story)
        correct_length = self.has_okay_length(user_story)
        can_be_processed = right_number_of_roles_means_ends and correct_ordering_of_role_means_ends and correct_length
        if not can_be_processed:
            return user_story, can_be_processed
        self.split_story_into_chunks(user_story)
        self.tokenise_and_pos_tag_chunks(user_story)
        return user_story, can_be_processed
    

    def check_only_one_role_means_ends(self, story: UserStory) -> bool:
        """
        Checks that there is only one role, one means, and one ends
        If there is more than one of any, an atomic violation is added
        """
        max_one_means = story.original_lower_text.count(MEANS_INDICATOR) <= 1
        max_one_ends = story.original_lower_text.count(ENDS_INDICATOR) <= 1
        
        if not max_one_means:
            story.add_defect(self.user_story_defect_types.atomic, self.user_story_error_messages.more_than_one_means)
        if not max_one_ends:
            story.add_defect(self.user_story_defect_types.atomic, self.user_story_error_messages.more_than_one_ends)

        return max_one_means and max_one_ends

    
    def check_role_means_ends_ordering(self, story: UserStory) -> bool:
        """
        Checks the ordering of the role, means, and ends
        Returns true if it is in the correct order (role -> means -> ends) otherwise false
        """
        role_position = story.original_lower_text.find(ROLE_INDICATOR)
        means_position = story.original_lower_text.find(MEANS_INDICATOR)
        ends_position = story.original_lower_text.find(ENDS_INDICATOR)

        role_before_means = role_position == -1 or means_position == -1 or role_position < means_position
        role_before_ends = role_position == -1 or ends_position == -1 or role_position < ends_position
        means_before_ends = means_position == -1 or ends_position == -1 or means_position < ends_position
        all_indicators_missing = role_position == -1 and means_position == -1 and ends_position == -1

        correct_ordering = (role_before_means and means_before_ends and role_before_ends) or all_indicators_missing

        if not correct_ordering:
            story.add_defect(self.user_story_defect_types.well_formed, self.user_story_error_messages.bad_ordering)

        return correct_ordering
    

    def has_okay_length(self, story: UserStory) -> bool:
        """
        Checks that the user story is in the right length range
        """
        words = story.original_lower_text.split(" ")
        too_big = len(words) > MAX_LENGTH

        if too_big:
            story.add_defect(self.user_story_defect_types.length, self.user_story_error_messages.too_long)

        return not too_big


    def split_story_into_chunks(self, story: UserStory) -> None:
        """
        Split a user story into chunks to get the role, means, and ends.
        """
        has_role = story.original_lower_text.find(ROLE_INDICATOR) != -1
        has_means = story.original_lower_text.find(MEANS_INDICATOR) != -1

        if has_role == has_means or (not has_role and has_means):
            self.extract_role(story)
            self.extract_means(story)
            self.extract_ends(story)
        elif has_role:
            self.find_potential_means(story)


    def tokenise_and_pos_tag_chunks(self, story: UserStory) -> None:
        """
        Splits the chunks of a user story into tokens and tag each token with a POS tag
        """
        self.tokenise_and_pos_tag_chunk(story, story.role, UserStoryPart.ROLE)
        self.tokenise_and_pos_tag_chunk(story, story.means, UserStoryPart.MEANS)
        self.tokenise_and_pos_tag_chunk(story, story.ends, UserStoryPart.ENDS)


    def tokenise_and_pos_tag_chunk(self, story: UserStory, chunk: str, part: UserStoryPart) -> None:
        """
        Take the role of a user story and split it into tokens and tag each token with a POS tag
        """
        if chunk != None:
            pos = self.nlp_service.tokenise_words(self.nlp_service.get_string_without_punctuation(chunk))
            self.add_pos_to_user_story(story, part, pos)
            

    def add_pos_to_user_story(self, story: UserStory, part: UserStoryPart, pos: list) -> None:
        """
        Add the parts of speech breakdown to the user story object
        """
        match part:
            case UserStoryPart.ROLE:
                story.role_pos = pos
            case UserStoryPart.MEANS:
                story.means_pos = pos
            case UserStoryPart.ENDS:
                story.ends_pos = pos

    
    def extract_role(self, story: UserStory) -> None:
        """
        Extract the role from the original story text.
        If there is no role, add it to the list of defects.
        """
        role_pos = story.original_lower_text.find(ROLE_INDICATOR)
        means_pos = story.original_lower_text.find(MEANS_INDICATOR)
        ends_pos = story.original_lower_text.find(ENDS_INDICATOR)
        role = None

        if role_pos != -1 and means_pos != -1:
            role = story.original_lower_text[role_pos:means_pos].strip()
        elif role_pos !=-1 and means_pos == -1 and ends_pos != -1:
            role = story.original_lower_text[role_pos:ends_pos].strip()
        elif role_pos !=-1 and means_pos == -1 and ends_pos == -1:
            role = story.original_lower_text[role_pos:].strip()
        else:
            role = self.find_user_persona_role(story.original_lower_text)
            if role == None:
                story.add_defect(self.user_story_defect_types.well_formed, self.user_story_error_messages.missing_role)
        story.role = role.lower() if role else None

    
    def find_user_persona_role(self, text: str) -> str:
        """
        Finds the word "as" followed by a proper noun, and returns up to this point. 
        This is to deal with the case where user personas are used instead of user types.
        """
        text_pos = self.nlp_service.tokenise_words(text)
        for i in range(1, len(text_pos)):
            curr = text_pos[i]
            prev = text_pos[i-1][0].lower()
            if self.nlp_service.is_proper_noun(curr) and prev == ROLE_INDICATOR_USING_PERSONAS:
                return " ".join([word[0] for word in text_pos[:i+1]])
        return None


    def extract_means(self, story: UserStory) -> None:
        """
        Extract the means from the original story text.
        If there is no means, add it to the list of defects.
        """
        means_pos = story.original_lower_text.find(MEANS_INDICATOR)
        ends_pos = story.original_lower_text.find(ENDS_INDICATOR)
        means = None

        if means_pos != -1:
            if ends_pos != -1:
                means = story.original_lower_text[means_pos:ends_pos].strip()
            else:
                means = story.original_lower_text[means_pos:].strip()
        else:
            story.add_defect(self.user_story_defect_types.well_formed, self.user_story_error_messages.missing_means)

        story.means = means if means else None
    

    def find_potential_means(self, story: UserStory) -> None:
        """
        Looks for a potential means if there is no means found using the indicator
        Tags the user story with a indicator to say the means is potential, not confirmed
        """
        story_text = self.remove_ends(story)
        pos = self.nlp_service.tokenise_words(self.nlp_service.get_string_without_punctuation(story_text))
        story_text_list = story_text.split()
        potential_means_found = False

        if pos and len(pos) > 0:
            first_noun_position = self.find_position_of_end_of_noun(pos, story_text_list)
            story.role = ' '.join(story_text_list[:first_noun_position])
            story_text_list = story_text_list[first_noun_position:]
            pos = pos[first_noun_position:]
            found_verbs, found_nouns = self.nlp_service.has_required_number_verb_and_noun(pos, 1, 1)
            potential_means_found = found_verbs and found_nouns

            if potential_means_found:
                story.means = ' '.join(story_text_list)
                story.using_potential_means = True
            else:
                story.role = story.role + " " + ' '.join(story_text_list)
        if not pos or not potential_means_found:
            story.add_defect(self.user_story_defect_types.well_formed, self.user_story_error_messages.missing_means)


    def remove_ends(self, story: UserStory) -> str:
        """
        Removes the role indicator and the ends from a user story text
        Returns the story text as a string and a list
        """
        story_text = story.original_lower_text
        ends = self.extract_ends(story)
        story_text = story_text.replace(ends, "")
        return story_text.strip()


    def find_position_of_end_of_noun(self, pos: list, story_text_list: str) -> int:
        """
        Given a list of tokens with their associated POS tags
        Return the position of the first noun (1-indexed not 0-indexed)
        """
        word_position = 0
        done = False

        while not done and word_position < len(pos):
            if self.nlp_service.is_noun(pos[word_position], True):
                marker = word_position
                check_ahead_done = False
                while not check_ahead_done and marker < len(pos):
                    if not "," in story_text_list[marker-1] and not pos[marker][0] == "i":
                        marker += 1
                    else:
                        word_position = marker - 1
                        check_ahead_done = True
                done = True
            else:
                word_position += 1
        
        return word_position + 1

    
    def extract_ends(self, story: UserStory) -> str:
        """
        Extract the ends from the original story text.
        If there is no ends, add it to the list of defects.
        Return the user story without the ends.
        """
        ends_pos = story.original_lower_text.find(ENDS_INDICATOR)
        ends = None

        if ends_pos != -1:
            ends = story.original_lower_text[ends_pos:].strip()
        else:
            ends = self.find_potential_ends(story) if story.means != None else None
            if ends == None:
                story.add_defect(self.user_story_defect_types.well_formed, self.user_story_error_messages.missing_ends)

        story.ends = ends if ends else None
        return story.original_lower_text[ends_pos:].strip() if ends_pos != -1 else ""
    

    def find_potential_ends(self, story: UserStory, min_nouns: int = 1, min_verbs: int = 2) -> str:
        """
        If only an ends is missing, a potential one can be found by looking for just the word 'so' after the noun and 2 verbs in the means
        Returns the ends string if one is found, otherwise nothing
        """
        word_list = story.means.split()
        means_pos = story.means_pos

        total_nouns = 0
        total_verbs = 0

        position = 0

        for token in means_pos:
            if self.nlp_service.is_noun(token, True):
                total_nouns += 1
            if self.nlp_service.is_verb(token):
                total_verbs += 1
            if total_verbs >= min_verbs and total_nouns >= min_nouns:
                break
            position += 1
        ends_list = word_list[position+1:]

        try:
            ends_start_pos = ends_list.index(POTENTIAL_ENDS_INDICATOR)
            story.using_potential_ends = True
            story.means = ' '.join(word_list[:ends_start_pos+position + 1])
            return ' '.join(ends_list[ends_start_pos:])
        except ValueError:
            return None

