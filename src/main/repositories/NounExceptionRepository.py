VERB_NOUN_EXCEPTION_FILE = "/main/data/noun_exceptions.txt"

class NounExceptionRepository():

    def __init__(self, data_path) -> None:
        self.full_path = data_path + VERB_NOUN_EXCEPTION_FILE


    def get_noun_exceptions(self) -> list:
        """
        Add all noun exceptions to the list of words from the .txt file
        """
        words_list = []
        try:
            with open(self.full_path, 'r') as file:
                for line in file:
                    word = line.strip()
                    if word:
                        words_list.append(word)
        except FileNotFoundError:
            print(f"The file {self.full_path} was not found.")
        except Exception as e:
            print(f"An error occurred: {e}")
        
        return words_list
    

    def add_noun_exception(self, word: str) -> None:
        """
        Add new word to noun exception list
        """
        with open(self.full_path, 'a') as file:
            file.write('\n' + word)


    