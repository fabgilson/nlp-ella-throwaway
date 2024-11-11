from datetime import datetime
import json
import os
from flask import request

from main.models import UserStory
from main.services.ambiguity.AmbiguityAnalyser import AmbiguityAnalyser
from main.services.userstories.UserStoryPreprocessor import UserStoryPreprocessor
from main.services.userstories.UserStoryAnalyser import UserStoryAnalyser

class UserStoryController():

    def __init__(self, user_story_preprocessor: UserStoryPreprocessor, user_story_analyser: UserStoryAnalyser, ambiguity_analyser: AmbiguityAnalyser) -> None:
        self.user_story_preprocessor = user_story_preprocessor
        self.user_story_analyser = user_story_analyser
        self.ambiguity_analyser = ambiguity_analyser

    
    def prepare_results(self, user_story: UserStory):
        """
        Prepare the defects to be returned by the API
        """
        return_list = []
        for defect in user_story.defects:
            new_defect = {"title": defect, "description": user_story.defects[defect]}
            return_list.append(new_defect)
        return return_list
    

    def log_attempt(self, acs: list, results: list, us_number: str) -> None:
        """
        Log attempts in json file
        """
        datetime_key = datetime.now().isoformat()

        attempt = {
            "type": "us",
            "us_number": us_number,
            "input": acs,
            "output": results
        }

        log_file = "prediction_log.json"
            
        if os.path.exists(log_file):
            with open(log_file, "r") as f:
                log_data = json.load(f)
        else:
            log_data = {}
        
        log_data[datetime_key] = attempt

        with open(log_file, "w") as f:
            json.dump(log_data, f, indent=4)


    # POST /story
    def check_user_story(self) -> dict:
        """
        Takes a user story and returns a dictionary of found defects.
        """
        data = request.get_json()
        story_text = data['story_text']
        try:
            us_number = data['us_number']
        except:
            us_number = 0
        user_story, can_be_processed = self.user_story_preprocessor.pre_process_story_text(story_text)
        if can_be_processed:
            user_story = self.user_story_analyser.analyse_user_story(user_story)
            user_story = self.ambiguity_analyser.is_unambiguous(user_story)
        return_results = self.prepare_results(user_story)
        self.log_attempt(story_text, return_results, us_number)
        return return_results
