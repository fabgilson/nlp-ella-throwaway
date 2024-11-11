class ACErrorMessages():

    def __init__(self) -> None:
        # integrous
        self.missing_context = "The AC needs to have a GIVEN clause"
        self.missing_event = "The AC needs to have a WHEN clause"
        self.missing_outcome = "The AC needs to have a THEN clause"
        self.out_of_order = "The required clauses of the AC are out of order, consider splitting the AC"
        self.context_missing_noun_or_verb = "The GIVEN chunk of the AC should have at least one verb and at least one noun"
        self.event_missing_noun_or_verb = "The WHEN chunk of the AC should have at least one verb and at least one noun"
        self.outcome_missing_noun_or_verb = "The THEN chunk of the AC should have at least one verb and at least one noun"

        # essential
        self.more_than_one_context = "The AC should only have one GIVEN clause"
        self.more_than_one_event = "The AC should only have one WHEN clause"
        self.more_than_one_outcome = "The AC should only have one THEN clause"
        self.separating_punctuation = "The AC should not have separating punctuation, ie. it should only be once sentence"
        self.info_in_brackets = "The AC should not have more information than necessary, ie. information in brackets. If the information in the brackets is necessary, then you should expand out the brackets."

        # singular
        self.list_in_ac = "There is a list in the AC. If this is a OR list, then you should split up the AC. If it is an AND list, then you should split it into separate AND clauses."


    def full_duplicates(self, indices: list) -> str:
        return f"The following ACs are duplicates: {[index + 1 for index in indices]}"