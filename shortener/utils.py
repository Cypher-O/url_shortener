from rest_framework.response import Response
from rest_framework import status

class APIResponse:
    @staticmethod
    def success(data=None, message="Success", status_code=status.HTTP_200_OK):
        response_data = {
            "code": 0,
            "status": "success",
            "message": message,
            "data": data if data is not None else []
        }
        return Response(response_data, status=status_code)

    @staticmethod
    def error(message="An error occurred", code=1, status_code=status.HTTP_400_BAD_REQUEST):
        response_data = {
            "code": code,
            "status": "error",
            "message": message,
            "data": []
        }
        return Response(response_data, status=status_code)