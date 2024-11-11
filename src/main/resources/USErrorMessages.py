class USErrorMessages():

    def __init__(self, max_length: int = 0) -> None:
        # well-formed errors
        self.missing_role = "The user story is missing an entity that is requesting the feature."
        self.missing_means = "The user story is missing a feature being requested."
        self.missing_ends = "The user story is missing a reason for the feature being requested."
        self.means_doesnt_start_with_i = "The first word of the means should be 'I'"
        self.bad_ordering = "The user story should be ordered as follows: entity requesting the feature, the feature being requested, the reason for the feature being requested."

        # full sentence errors
        self.role_doesnt_end_with_noun = "The entity should have a noun as the last word"
        self.means_missing_second_verb = "The feature should involve an action."
        self.means_missing_noun = "The feature should involve an object."
        self.ends_missing_words = "There needs to be reasoning for the feature"

        # atomic errors
        self.more_than_one_role = "There is more than one entity requesting the feature."
        self.more_than_one_means = "There is more than one feature being requested."
        self.more_than_one_ends = "There is more than one reasoning for the feature."
        self.list_of_verbs_in_means = "There is a list of verbs, indicating more than one feature is being requested."

        # minimal errors
        self.has_separating_punctuation = "There should not be text after separating punctuation."
        self.has_brackets = "There is information inside brackets, if this is necessary information then consider splitting the user story. Otherwise you should remove the brackets."

        # uniform errors
        self.not_uniform = "The user story should be in the format 'As a <role> I want <feature> so that <rationale>'"

        # length errors
        self.too_long = f"The user story should be no more than {max_length} words long"
