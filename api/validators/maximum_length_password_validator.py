from django.utils.translation import gettext as _
from rest_framework.exceptions import ValidationError


class MaximumLengthValidator:
    """
    Validate that the password has less than 50 characters.
    """

    def __init__(self, max_length=50):
        self.max_length = max_length

    def validate(self, password: str, user=None) -> None:
        if len(password) > self.max_length:
            raise ValidationError(
                _("This password must contain less than %(max_length)d characters."),
                code="password_too_long",
                params={"max_length": self.max_length},
            )

    def get_help_text(self) -> str:
        return _(
            "Your password must contain less than %(max_length)d characters."
            % {"max_length": self.max_length}
        )
