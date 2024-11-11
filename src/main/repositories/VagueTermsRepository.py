VAGUE_TERMS_FILE = "/main/data/vague_terms.txt"

class VagueTermsRepository():

    def __init__(self, data_path) -> None:
        self.full_path = data_path + VAGUE_TERMS_FILE


    def get_vague_terms(self) -> list:
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


    