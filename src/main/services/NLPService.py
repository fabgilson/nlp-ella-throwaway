import nltk
import re

from nltk.tokenize import word_tokenize, sent_tokenize
from nltk import pos_tag
from nltk.corpus import wordnet as wn
from nltk.chunk import RegexpParser
from main.services.WordlistService import WordlistService

class NLPService():

    def __init__(self, wordlist_service: WordlistService) -> None:
        self.wordlist_service = wordlist_service
        self.pos_service = POS(wordlist_service)
        self.brackets_service = Brackets()
        self.punctuation_service = Punctuation()
        self.list_service = Lists(self.pos_service, self.wordlist_service, self.punctuation_service)
        self.ambiguity_service = Ambiguity(self.pos_service)
        

    def tokenise_words(self, text: str) -> list:
        """
        Take some text and return a list of tokens with their associated POS tag
        """
        return self.pos_service.tokenise_words(text)
    
    def is_noun(self, token: tuple, ignore_i_as_noun: bool = False) -> bool:
        """
        Check if a NLTK POS token is a noun
        """
        return self.pos_service.is_noun(token, ignore_i_as_noun)

    def is_verb(self, token: tuple) -> bool:
        """
        Check if a NLTK POS token is a verb
        """
        return self.pos_service.is_verb(token)
    
    def is_modal(self, token: tuple) -> bool:
        """
        Check if a NLTK POS token is a modal verb(?)
        """
        return self.pos_service.is_modal(token)
    
    def is_proper_noun(self, token: tuple) -> bool:
        """
        Check if a NLTK POS token is a proper noun
        """
        return self.pos_service.is_proper_noun(token)

    def is_potential_noun_or_verb(self, token: tuple) -> bool:
        """
        Check if a word is either a verb or noun, and if it is in the list of noun/verb exceptions
        """
        return self.pos_service.is_potential_noun_or_verb(token)
    
    def extract_noun_phrases(self, text: str) -> list:
        """
        Extract a list of noun phrases from the given 
        Returns the list of noun phrases
        """
        return self.pos_service.extract_noun_phrases(text)
    
    def has_required_number_verb_and_noun(self, pos: str | None, required_nouns: int, required_verbs: int, ignore_i_as_noun: bool = False) -> tuple:
        """
        Checks that a given list of POS tokens has the number of required nouns and number of required verbs
        """
        return self.pos_service.has_required_number_verb_and_noun(pos, required_nouns, required_verbs, ignore_i_as_noun)

    def get_string_without_punctuation(self, text: str) -> str:
        """
        Removes punctuation from a string 
        Useful for some parts of analysing chunks of text where punctuation doesn't matter
        """
        return self.punctuation_service.get_string_without_punctuation(text)
    
    def remove_all_quotes_from_string(self, input_string):
        """
        Removes all text inside quote marks, including the quote marks, from a string
        """
        return self.punctuation_service.remove_all_quotes_from_string(input_string)
    
    def has_separating_punctuation_with_following_text(self, text: str) -> bool:
        """
        Checks if there is separating punctuation in the given string with text following it 
        True if there is, otherwise false
        """
        return self.punctuation_service.has_separating_punctuation_with_following_text(text)
    
    def remove_references(self, text: str) -> str:
        """
        Removes indicators of references from text 
        For use when checking for brackets containing information: should remove things like [1], [2] from strings
        """
        return self.brackets_service.remove_references(text)

    def has_brackets_containing_information(self, text: str) -> list:
        """
        Extract text within well-formed brackets in a given piece of text. Returns a list of texts found within brackets.
        """
        return self.brackets_service.has_brackets_containing_information(text)
    
    def check_for_lists(self, chunk: str | None) -> bool:
        """
        Determines whether or not there is a list of items in a string
        True if there is a list
        """
        return self.list_service.check_for_lists(chunk)
    

class POS():

    def __init__(self, wordlist_service: WordlistService) -> None:
        self.wordlist_service = wordlist_service
        self.noun = ['NN', 'NNS', 'NNP', 'NNPS']
        self.verb = ['VB', 'VBD', 'VBG', 'VBN', 'VBP', 'VBZ']
        self.proper_noun = "NNP"
        self.modal = "MD"
        self.noun_phrase_grammar = "NP: {<DT>?<JJ>*<NN.*>+}"


    def tokenise_words(self, text: str) -> list:
        """
        Take some text and return a list of tokens with their associated POS tag
        """
        pos = []
        for sent in sent_tokenize(text):
            wordtokens = word_tokenize(sent)
            pos += nltk.pos_tag(wordtokens)
        return pos


    def is_noun(self, token: tuple, ignore_i_as_noun: bool = False) -> bool:
        """
        Check if a NLTK POS token is a noun
        """
        is_noun = token[1] in self.noun or token[0] in self.wordlist_service.get_verb_exceptions()
        if ignore_i_as_noun:
            is_noun = (is_noun and token[0] not in self.wordlist_service.get_noun_exceptions()) or token[0] in self.wordlist_service.get_verb_exceptions()
        return is_noun


    def is_verb(self, token: tuple) -> bool:
        """
        Check if a NLTK POS token is a verb
        """
        is_verb = token[1] in self.verb and token[0] not in self.wordlist_service.get_verb_exceptions()
        return is_verb
    

    def is_modal(self, token: tuple) -> bool:
        """
        Check if a NLTK POS token is a modal verb(?)
        """
        return token[1] == self.modal
    

    def is_proper_noun(self, token: tuple) -> bool:
        """
        Check if a NLTK POS token is a proper noun
        """
        return token[1] == self.proper_noun
    

    def is_potential_noun_or_verb(self, token: tuple) -> bool:
        """
        Check if a word is either a verb or noun, and if it is in the list of noun/verb exceptions
        """
        return token[0] in self.wordlist_service.get_verb_noun_exceptions() and (self.is_noun(token) or self.is_verb(token))
    

    def extract_noun_phrases(self, text: str) -> list:
        """
        Extract a list of noun phrases from the given 
        Returns the list of noun phrases
        """
        words = word_tokenize(text)
        pos_tags = pos_tag(words)
        chunk_parser = RegexpParser(self.noun_phrase_grammar)
        tree = chunk_parser.parse(pos_tags)
        noun_phrases = []
        for subtree in tree:
            if type(subtree) == nltk.Tree and subtree.label() == 'NP':
                noun_phrases.append(" ".join([word for word, pos in subtree.leaves()]))
        return noun_phrases
    

    def has_required_number_verb_and_noun(self, pos: str | None, required_nouns: int, required_verbs: int, ignore_i_as_noun: bool = False) -> tuple:
        """
        Checks that a given list of POS tokens has the number of required nouns and number of required verbs
        """
        if pos == None:
            return (True, True)
        
        verbs = []
        nouns = []
        for token in pos:
            if self.is_noun(token, ignore_i_as_noun):
                nouns.append(token)
            elif self.is_verb(token):
                verbs.append(token)
        found_verbs = len(verbs) >= required_verbs 
        found_noun = len(nouns) >= required_nouns
        if not found_verbs or not found_noun:
            if found_noun != found_verbs:
                found_verbs, found_noun = self.get_potential_verbs_nouns(found_noun, found_verbs, verbs, nouns, required_verbs, required_nouns)
        return (found_verbs, found_noun)
    

    def get_potential_verbs_nouns(self, found_noun, found_verbs, verbs, nouns, min_verbs, min_nouns) -> tuple:
        """
        Make calls to get potential verbs and nouns if necessary
        """
        if not found_noun and found_verbs:
            found_noun = self.check_potential_verbs_or_nouns(verbs, nouns, min_nouns, min_verbs)
        elif not found_verbs and found_noun:
            found_verbs = self.check_potential_verbs_or_nouns(nouns, verbs, min_verbs, min_nouns)

        return found_verbs, found_noun
    

    def check_potential_verbs_or_nouns(self, found: list, not_found: list, min_not_found: int, min_found: int) -> bool:
        """
        Given a list that has enough of either verbs or nouns found and another list that doesn't have enough of the other
        Returns true if there are enough found in the opposite list that could be changed between verb/noun based on exceptions list
        """
        num_missing = min_not_found - len(not_found)
        num_spare = len(found) - min_found
        if num_missing > num_spare:
            return False

        extras_found = 0
        for token in found:
            extras_found += 1 if self.is_potential_noun_or_verb(token) else 0

        return extras_found >= num_missing

    
class Brackets():

    def __init__(self) -> None:
        self.matching_brackets = {')': '(', '}': '{', ']': '['}

    def remove_references(self, text: str) -> str:
        """
        Removes indicators of references from text
        For use when checking for brackets containing information: should remove things like [1], [2] from strings
        """
        cleaned_text = re.sub(r'\[\d+\]', '', text)
        return cleaned_text


    def has_brackets_containing_information(self, text: str) -> list:
        """
        Extract text within well-formed brackets in a given piece of text.
        Returns a list of texts found within brackets.
        """
        text = self.remove_references(text)
        matching_bracket = self.matching_brackets
        stack = []
        results = []
        current_text = []

        for char in text:
            if char in matching_bracket.values():
                stack.append((char, False))
                current_text.append([])
            elif char in matching_bracket.keys():
                if stack and stack[-1][0] == matching_bracket[char]:
                    stack.pop()
                    text_in_bracket = ''.join(current_text.pop())
                    results.append(text_in_bracket)
                    if stack:
                        current_text[-1].append(text_in_bracket)
                else:
                    return []
            elif stack:
                current_text[-1].append(char)
        return [result for result in results if result != ""]  


class Punctuation():

    def __init__(self) -> None:
        self.separating_punctuation = [". ", "- ", "; ", "? ", "* ", "! "]
        self.ignore_punctuation = ["e.g.", "e.g", "eg.", "i.e.", "i.e", "ie.", "a.k.a.", "a.k.a", "dr.", "miss.", "ms.", "mrs.", "mr."]

    def has_separating_punctuation_with_following_text(self, text: str) -> bool:
        """
        Checks if there is separating punctuation in the acceptance criteria with text following it
        True if there is, otherwise false
        """
        split_text = self.split_on_punctuation(text)
        for i in range(1, len(split_text)):
            if len(split_text[i]) > 0 and len(split_text[i-1]) > 0:
                return True
        return False


    def split_on_punctuation(self, text: str) -> list:
        """
        Splits a piece of text into a list of pieces with the separating punctuation gone
        """
        ignore_punctuation_pattern = re.compile('|'.join(re.escape(punct) for punct in self.ignore_punctuation))
        text = ignore_punctuation_pattern.sub("", text)
        pattern = '|'.join(map(re.escape, self.separating_punctuation))
        split_list = re.split(pattern, text)
        split_list = [substr for substr in split_list if substr]
        return split_list
    

    def get_string_without_punctuation(self, text: str) -> str:
        """
        Removes punctuation from a string
        Useful for some parts of analysing chunks of text where punctuation doesn't matter
        """
        return re.sub(r'[^a-zA-Z\s]', '', text)
    

    def remove_all_quotes_from_string(self, input_string):
        """
        Removes all text inside quote marks, including the quote marks, from a string
        """
        pattern = r'[\"“‘\'][^\"“”‘’\']+[\"”’\']'
        result = re.sub(pattern, '', input_string)
        return result.replace("  ", " ").strip()
    

class Lists():

    def __init__(self, pos_service: POS, wordlist_service: WordlistService, punctuation_service: Punctuation) -> None:
        self.list_indicators = [", ", " or ", " and "] 
        self.list_conjuctions = ["or", "and"]
        self.pos_service = pos_service
        self.wordlist_service = wordlist_service
        self.punctuation_service = punctuation_service


    def check_for_lists(self, chunk: str | None) -> bool:
        """
        Determines whether or not there is a list of items in a string
        True if there is a list
        """
        if chunk != None:
            text = self.punctuation_service.remove_all_quotes_from_string(chunk)
            noun_phrases = self.pos_service.extract_noun_phrases(text)
            potential_lists = self.get_potential_lists(text, noun_phrases)
            return self.has_list(text, potential_lists)
        else:
            return False


    def get_potential_lists(self, text: str, noun_phrases: list) -> dict: 
        """
        Takes list of noun phrases from the sentence
        Returns a dictionary where each item is a list of noun phrases that are close together in the original text
        """
        list_items = {}
        list_counter = 0
        for phrase in noun_phrases:
            try:
                curr = text.index(phrase)
                next_phrase = noun_phrases[noun_phrases.index(phrase)+1]
                next = text.index(next_phrase)
                diff = next - (curr + len(phrase))
                if diff in range(-5, 10):
                    if list_counter in list_items:
                        if phrase not in list_items[list_counter]:
                            list_items[list_counter].append(phrase)
                        if next_phrase not in list_items[list_counter]:
                            list_items[list_counter].append(next_phrase)
                    else:
                        list_items[list_counter] = [phrase]
                        if next_phrase not in list_items[list_counter]:
                            list_items[list_counter].append(next_phrase)
                elif list_counter in list_items:
                    list_counter += 1
            except:
                continue
        return list_items


    def has_list(self, text: str, potential_lists: dict) -> bool:
        """
        Given a dictionary of close noun phrases, check if a comma, 'or', or 'and' show uo between them
        If this occurs, then there is a potential list in the string
        Returns true if there is a potential list
        """
        has_list = False
        for list_num in potential_lists:
            list_items = potential_lists[list_num]
            if len(list_items) >= 2:
                for item in list_items:
                    try:
                        end_of_curr = text.index(item) + len(item)
                        start_of_next = text.index(list_items[list_items.index(item)+1])
                        between_items = text[end_of_curr:start_of_next]
                        if not has_list:
                            has_list = bool([ele for ele in self.list_indicators if(ele in between_items)])
                    except:
                        continue

        return has_list
    

    def has_list_of_verbs(self, text: str) -> bool:
        """
        Checks for the pattern: <verb> and/or <verb> indicating a list of actions
        """
        if text == None:
            return False
        tokens = self.pos_service.tokenise_words(text)
        for i in range(len(tokens)):
            if self.pos_service.is_verb(tokens[i]) or tokens[i][0] in self.wordlist_service.get_verb_noun_exceptions():
                if i+2 < len(tokens) and tokens[i+1][0] in self.list_conjuctions and self.pos_service.is_verb(tokens[i+2]):
                    return True
        return False



class Ambiguity():

    def __init__(self, pos_service: POS) -> None:
        self.comparatives = ['JJR', 'RBR']
        self.superlatives = ['JJS', 'RBS']
        self.anaphora_tags = ['PRP', 'PRP$']
        self.anaphora_exceptions = ["my", "i", "me", "our", "offline"]
        self.than = 'than'
        self.comparative_exceptions = ["lower"]
        self.superlative_exceptions = ["least, greatest"]
        self.pos_service = pos_service


    def find_comparatives_superlatives(self, sentence: str) -> tuple:
        """
        Finds all superlatives and comparative adverbs and adjectives in a sentence
        Returns two separate lists, one of all comparative words and one of all superlative words
        """
        tagged_words = self.pos_service.tokenise_words(sentence)
        
        comparatives = []
        superlatives = []
    
        for i, (word, tag) in enumerate(tagged_words):
            next_four_words = [tagged_words[j][0] for j in range(i+1, min(i+5, len(tagged_words)))]
            if tag in self.comparatives and self.than not in next_four_words and word not in self.comparative_exceptions:
                comparatives.append(word)
            elif tag in self.superlatives and word not in self.superlative_exceptions:
                superlatives.append(word)
        
        return comparatives, superlatives
    

    def find_anaphora_indicators(self, sentence: str | None) -> list:
        """
        Finds instances of anaphora in a sentence (using words without explicitly knowing what is being referenced)
        Returns list of words indicating anaphora
        """
        if not sentence:
            return []
        
        tagged_words = self.pos_service.tokenise_words(sentence)

        anaphora_words = []
        for word, tag in tagged_words:
            if tag in self.anaphora_tags and word not in self.anaphora_exceptions:
                anaphora_words.append(word)

        return anaphora_words
        

