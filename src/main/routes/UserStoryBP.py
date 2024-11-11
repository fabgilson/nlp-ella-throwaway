from flask import Blueprint

from main.controllers.UserStoryController import UserStoryController

class UserStoryBP():

    def __init__(self, user_story_controller: UserStoryController) -> None:
        self.user_story_controller = user_story_controller
        self.user_story_bp = Blueprint('user_bp', __name__)
        self.register_routes()

    def register_routes(self) -> None:
        self.user_story_bp.route('', methods=['POST'])(self.user_story_controller.check_user_story)

    def user_story_bp(self) -> Blueprint:
        return self.user_story_bp