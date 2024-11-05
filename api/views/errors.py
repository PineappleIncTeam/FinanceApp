from rest_framework.exceptions import APIException


class CategoryWithOperationsError(APIException):
    status_code = 400
    default_detail = "Can not delete category with existing operations."
    default_code = "operations_exists"
