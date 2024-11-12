from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_400_BAD_REQUEST


class CategoryWithOperationsError(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "Can not delete category with existing operations."
    default_code = "operations_exists"


class TargetIsClosedError(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "The target is closed."
    default_code = "closed_target"


class TargetInProgressError(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "The target is not achieved."
    default_code = "target_in_progress"


class NoMoneyToReturnError(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "There is no money to return."
    default_code = "no_money_to_return"
