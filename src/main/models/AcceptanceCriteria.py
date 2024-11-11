class AcceptanceCriteria():

    def __init__(self, original_lower_text, original_text) -> None:
        self.context = None
        self.event = None
        self.outcome = None
        self.original_text = original_text
        self.original_lower_text = original_lower_text
        self.defects = {}
        self.context_pos = []
        self.event_pos = []
        self.outcome_pos = []
        self.ac_number = None
        self.context_and_clauses = []
        self.event_and_clauses = []
        self.outcome_and_clauses = []

    def add_defect(self, type: str, error_message: str) -> None:
        """
        Add a defect to a dictionary of found defects
        """
        if type in self.defects:
            errors = self.defects[type]
            errors.append(error_message)
            self.defects[type] = errors
        else:
            self.defects[type] = [error_message]

    def to_string(self) -> str:
        return f"Context: {self.context}, Event: {self.event}, Outcome: {self.outcome}"