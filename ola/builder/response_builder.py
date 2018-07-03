from rest_framework import status
from rest_framework.response import Response


class ResponseBuilder:

    def __init__(self):
        self.response = {}
        self.response_message = ""
        self.response_status = 1
        self.status = status.HTTP_200_OK

    def success(self):
        self.response_status = 1
        return self

    def failure(self):
        self.response_status = 0
        return self

    def message(self, message):
        self.response_message = message
        return self

    def response_data(self, data={}):
        self.response = data
        return self

    def ok_200(self):
        self.status = status.HTTP_200_OK
        return self

    def not_found_404(self):
        self.status = status.HTTP_404_NOT_FOUND
        return self

    def bad_request_400(self):
        self.status = status.HTTP_400_BAD_REQUEST
        return self

    def get_response(self):
        content = self.get_json()
        return Response(content, status=self.status)

    def get_json(self):
        result = dict(response_code=self.response_status,
                      response_message=self.response_message,
                      response=self.response)
        return result
