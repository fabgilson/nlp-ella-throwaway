from flask import Blueprint

from main.controllers.WordController import WordController

class WordlistsBP():

    def __init__(self, word_controller: WordController) -> None:
        self.word_controller = word_controller
        self.word_list_bp = Blueprint('word_bp', __name__)
        self.register_routes()

    def register_routes(self) -> None:
        self.word_list_bp.route('/noun', methods=['POST'])(self.word_controller.add_noun_exception)
        self.word_list_bp.route('/nounverb', methods=['POST'])(self.word_controller.add_noun_verb_exception)
        self.word_list_bp.route('/verb', methods=['POST'])(self.word_controller.add_verb_exception)

    def word_list_bp(self) -> Blueprint:
        return self.word_list_bp