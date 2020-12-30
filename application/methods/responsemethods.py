from application.models.responsetime import Responsetime
from application.utils.exceptions import CustomException
from application.utils.extensions import db

class ResponseMethods:
    #
    def get_responses_filtered_by_date(self, urlid):
        responses = Responsetime.query.filter(Responsetime.urlid == urlid)
        filtered_responses = self.filter_responses_by_date(responses)
        return filtered_responses

    def filter_responses_by_date(self, responses):
        dict_responses = [response.to_dict() for response in responses]
        sorted_responses = sorted(dict_responses, key=lambda x: x['timestamp'], reverse=True)
        return sorted_responses
