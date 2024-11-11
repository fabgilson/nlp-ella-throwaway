from flask import Blueprint

from main.controllers.AcceptanceCriteriaController import AcceptanceCriteriaController

class AcceptanceCriteriaBP():

    def __init__(self, acceptance_criteria_controller: AcceptanceCriteriaController) -> None:
        self.acceptance_criteria_controller = acceptance_criteria_controller
        self.acceptance_criteria_bp = Blueprint('ac_bp', __name__)
        self.register_routes()

    def register_routes(self) -> None:
        self.acceptance_criteria_bp.route('', methods=['POST'])(self.acceptance_criteria_controller.check_acceptance_criteria)

    def acceptance_criteria_bp(self) -> Blueprint:
        return self.acceptance_criteria_bp