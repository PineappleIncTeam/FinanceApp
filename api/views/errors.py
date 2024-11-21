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


class ExceedingTargetAmountError(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "The target amount has been exceeded."
    default_code = "target_amount_exceeding"


class InvalidTargetOperationDateError(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "Can't create target operation before creating the target."
    default_code = "invalid_target_operation_date"


class TargetArchievedError(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_detail = "Can't create operation for an archieved target."
    default_code = "target_archieved"
