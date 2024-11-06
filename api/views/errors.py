from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class CategoryWithOperationsError(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "Can not delete category with existing operations."
    default_code = "operations_exists"
