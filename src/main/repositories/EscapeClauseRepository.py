ESCAPE_CLAUSES_FILE = "/main/data/escape_clauses.txt"

class EscapeClauseRepository():

    def __init__(self, data_path) -> None:
        self.full_path = data_path + ESCAPE_CLAUSES_FILE


    def get_escape_clauses(self) -> list:
        """
        Gets a python list of all words from the vague terms text file
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
    