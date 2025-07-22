from rest_framework import exceptions, status

class CustomError(exceptions.APIException):
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    default_detail = "A server error occurred."

    def __init__(self, data, status_code):
        if status_code is not None:
            self.status_code = status_code

        if data is not None:
            self.detail = data
        else:
            self.detail = {
                "status": 0,
                "message": self.default_detail,
            }
