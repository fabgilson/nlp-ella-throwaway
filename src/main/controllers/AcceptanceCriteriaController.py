from datetime import datetime
import json
import os
from flask import request

from main.services.acceptancecriteria.AcceptanceCriteriaPreprocessor import AcceptanceCriteriaPreprocessor
from main.services.acceptancecriteria.AcceptanceCriteriaAnalyser import AcceptanceCriteriaAnalyser
from main.resources.ACErrorTypes import ACErrorTypes
from main.services.ambiguity.AmbiguityAnalyser import AmbiguityAnalyser

class AcceptanceCriteriaController():

    def __init__(self, acceptance_criteria_preprocessor: AcceptanceCriteriaPreprocessor, acceptance_criteria_analyser: AcceptanceCriteriaAnalyser, ambiguity_analyser: AmbiguityAnalyser) -> None:
        self.acceptance_criteria_preprocessor = acceptance_criteria_preprocessor
        self.acceptance_criteria_analyser = acceptance_criteria_analyser
        self.ambiguity_analyser = ambiguity_analyser
        self.ac_error_types = ACErrorTypes()

    
    def prepare_defects_for_return(self, acceptance_criteria: list, uniqueness_defects: list):
        """
        Create a json response for the user
        """
        results_list = []
        for ac in acceptance_criteria:
            defects = []
            for defect in ac.defects:
                new_defect = {"title": defect, "descriptions": ac.defects[defect]}
                defects.append(new_defect)
            new_entry = {"title": f"AC {ac.ac_number + 1}", "defects": defects}
            results_list.append(new_entry)
        if len(uniqueness_defects) > 0:
            results_list.append({"title": self.ac_error_types.uniqueness, "defects": uniqueness_defects})
        return results_list
    

    def process_ac(self, ac_tuple):
        """
        Process an AC if it is able to be processed
        """
        ac, flag = ac_tuple
        if flag:
            return self.acceptance_criteria_analyser.analyse_acceptance_criteria(ac)
        else:
            return ac
        
    
    def log_attempt(self, acs: list, results: list, us_number: str) -> None:
        """
        Log attempts in json file
        """
        datetime_key = datetime.now().isoformat()

        attempt = {
            "type": "ac",
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


    # POST /ac
    def check_acceptance_criteria(self) -> dict:
        """
        Takes a list of ACs and returns a dictionary of found defects.
        """
        data = request.get_json()
        acceptance_criteria = data['acceptance_criteria']
        try:
            us_number = data['us_number']
        except:
            us_number = 0
        acs = [(ac, i) for i, ac in enumerate(acceptance_criteria)]
        processed_criteria = list(map(self.acceptance_criteria_preprocessor.pre_process_ac_text, acs))
        analysed_criteria = list(map(self.process_ac, processed_criteria))
        criteria_with_ambiguity_checks = list(map(self.ambiguity_analyser.is_unambiguous, analysed_criteria))
        uniqueness_defects = self.acceptance_criteria_analyser.unique_analyser.are_unique(criteria_with_ambiguity_checks)
        return_data = self.prepare_defects_for_return(criteria_with_ambiguity_checks, uniqueness_defects)
        self.log_attempt(acceptance_criteria, return_data, us_number)
        return return_data
        
