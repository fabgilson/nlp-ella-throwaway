QUANTIFIERS_FILE = "/main/data/quantifiers.txt"

class QuantifiersRepository():

    def __init__(self, data_path) -> None:
        self.full_path = data_path + QUANTIFIERS_FILE


    def get_quantifiers(self) -> list:
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


    