class UserStory():

    def __init__(self, original_lower_text, original_text) -> None:
        self.role = None
        self.means = None
        self.ends = None
        self.original_text = original_text
        self.original_lower_text = original_lower_text
        self.defects = {}
        self.role_pos = []
        self.means_pos = []
        self.ends_pos = []
        self.using_potential_means = False
        self.using_potential_ends = False

    def add_defect(self, type: str, error_message: str) -> None:
        """
        Add a defect to the dictionary of found defects
        """
        if type in self.defects:
            errors = self.defects[type]
            errors.append(error_message)
            self.defects[type] = errors
        else:
            self.defects[type] = [error_message]

    def to_string(self) -> str:
        return f"Role: {self.role}, Means: {self.means}, Ends: {self.ends}"