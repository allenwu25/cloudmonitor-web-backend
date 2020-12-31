from application.models.responsetime import Responsetime
from application.utils.exceptions import CustomException
from application.utils.extensions import db

import datetime

class ResponseMethods:
    #
    def get_responses_filtered_by_date(self, urlid):
        responses = Responsetime.query.filter(Responsetime.urlid == urlid)
        filtered_responses = self.filter_responses_by_date(responses)
        return filtered_responses

    def filter_responses_by_date(self, responses):
        dict_responses = [response.to_dict() for response in responses]
        sorted_responses = sorted(dict_responses, key=lambda x: datetime.datetime.fromisoformat(str(x['timestamp'])), reverse=False)
        return sorted_responses

    def delete_responses(self, urlid):
        try:
            Responsetime.query.filter_by(urlid=urlid).delete()
        except:
            raise CustomException("Error when deleting responses", 400)
