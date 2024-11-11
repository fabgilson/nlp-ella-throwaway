import os

from flask import Flask
from flask_cors import CORS

from main.controllers.AcceptanceCriteriaController import AcceptanceCriteriaController
from main.repositories.QuantifiersRespository import QuantifiersRepository
from main.repositories.VagueTermsRepository import VagueTermsRepository
from main.repositories.EscapeClauseRepository import EscapeClauseRepository
from main.repositories.VerbExceptionRepository import VerbExceptionRepository
from main.repositories.WeakVerbsRepository import WeakVerbsRepository
from main.routes.AcceptanceCriteriaBP import AcceptanceCriteriaBP
from main.routes.UserStoryBP import UserStoryBP
from main.routes.WordlistsBP import WordlistsBP
from main.repositories.VerbNounExceptionRepository import VerbNounExceptionRepository
from main.repositories.NounExceptionRepository import NounExceptionRepository
from main.services.acceptancecriteria.AcceptanceCriteriaAnalyser import AcceptanceCriteriaAnalyser
from main.services.acceptancecriteria.AcceptanceCriteriaPreprocessor import AcceptanceCriteriaPreprocessor
from main.services.ambiguity.AmbiguityAnalyser import AmbiguityAnalyser
from main.services.userstories.UserStoryPreprocessor import UserStoryPreprocessor
from main.services.userstories.UserStoryAnalyser import UserStoryAnalyser
from main.services.WordlistService import WordlistService
from main.services.NLPService import NLPService
from main.controllers.UserStoryController import UserStoryController
from main.controllers.WordController import WordController

def create_app():
    app = Flask(__name__)
    CORS(app)
    cors = CORS(app, resource={
        r"/*":{
            "origins":"*"
        }
    })
    app.config.from_object('config')

    base_path = os.path.dirname(os.path.realpath(__file__))

    # register repositories
    verb_noun_exception_repository = VerbNounExceptionRepository(base_path)
    noun_exception_repository = NounExceptionRepository(base_path)
    verb_exception_repository = VerbExceptionRepository(base_path)
    vague_terms_repository = VagueTermsRepository(base_path)
    escape_clause_repository = EscapeClauseRepository(base_path)
    quantifiers_repository = QuantifiersRepository(base_path)
    weak_verbs_repository = WeakVerbsRepository(base_path)

    # register services
    word_list_service = WordlistService(
        verb_noun_exception_repository, 
        noun_exception_repository, 
        verb_exception_repository, 
        vague_terms_repository,
        escape_clause_repository,
        quantifiers_repository,
        weak_verbs_repository
    )
    nlp_service = NLPService(word_list_service)
    user_story_preprocessor = UserStoryPreprocessor(nlp_service)
    user_story_analyser = UserStoryAnalyser(nlp_service, word_list_service)
    acceptance_criteria_preprocessor = AcceptanceCriteriaPreprocessor(nlp_service)
    acceptance_criteria_analyser = AcceptanceCriteriaAnalyser(nlp_service, word_list_service)
    ambiguity_analyser = AmbiguityAnalyser(nlp_service, word_list_service)

    # register controllers
    user_story_controller = UserStoryController(
        user_story_preprocessor, 
        user_story_analyser, 
        ambiguity_analyser
    )
    acceptance_criteria_controller = AcceptanceCriteriaController(
        acceptance_criteria_preprocessor, 
        acceptance_criteria_analyser, 
        ambiguity_analyser
    )
    word_controller = WordController(word_list_service)

    # create blueprints
    user_story_bp = UserStoryBP(user_story_controller)
    acceptance_criteria_bp = AcceptanceCriteriaBP(acceptance_criteria_controller)
    word_list_bp = WordlistsBP(word_controller)

    # register blueprints
    app.register_blueprint(user_story_bp.user_story_bp, url_prefix='/story')
    app.register_blueprint(acceptance_criteria_bp.acceptance_criteria_bp, url_prefix='/ac')
    app.register_blueprint(word_list_bp.word_list_bp, url_prefix='/word')

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(port=8000,debug=True)