class AmbiguityErrorMessages():

    def __init__(self) -> None:
        pass

    def superlative(self, superlatives: list) -> str:
        return f"You have used the following superlatives: {superlatives}. These can introduce ambiguity as they create subjectivity."
    
    def comparative(self, comparatives: list) -> str:
        return f"You have used the following comparatives: {comparatives}. These can introduce ambiguity as they create subjectivity."
    
    def vague_terms(self, vague_terms: list) -> str:
        return f"You have used the following terms: {vague_terms}. These can introduce ambiguity as they create some vagueness for the reader."
    
    def escape_clauses(self, escape_clauses: list) -> str:
        return f"You have used the following escape clauses: {escape_clauses}. These can introduce ambiguity as they show a lack of commitment to the idea presented."
    
    def anaphora(self, anaphora: list) -> str:
        return f"This contains anaphora, which is using pronouns or adjectives in place of an explicit reference to something. Consider replacing the following words with explicit references: {anaphora}. When these are used, it is ambiguous to the reader what is being referenced."
    
    def quantifiers(self, quantifiers: list) -> str:
        return f"You have used the following quantifiers: {quantifiers}. These introduce ambiguity as they create uncertainty about the scope of what is being described."
    
    def weakness(self, weak_verbs: list) -> str:
        return f"You have used the following weak verbs: {weak_verbs}. These introduce ambiguity as they create uncertainty."