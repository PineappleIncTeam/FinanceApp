from rest_framework.exceptions import APIException


class CategoryExistsError(APIException):
    status_code = 400
    default_detail = "The category already exists."
    default_code = "category_exists"
