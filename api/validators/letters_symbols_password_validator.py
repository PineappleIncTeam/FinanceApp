from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _


class EnglishLettersSymbolsPasswordValidator:
    """
    Validate that the password contains only english letters and any other symbols (ASCII [33, 126]).
    The password must contain at least one uppercase letter and at least one number.
    """

    def validate(self, password: str, user=None) -> None:
        digit = 0
        upper_letters = 0
        for item in password:
            if item.isdigit():
                digit += 1
                continue
            if ord(item) < 33 or ord(item) > 126:
                raise ValidationError(
                    _("Your password contains unsupported symbols."),
                    code="password_unsupported_symbols"
                )
            if 65 <= ord(item) <= 90:
                upper_letters += 1

        if not digit or not upper_letters:
            raise ValidationError(
                _("Your password doesn't contain at least one uppercase letter or at least one number"),
                code="password_no_upper_symbols_no_digits"
            )

    def get_help_text(self) -> str:
        return _(
            """
            Your password should contain only english letters or
            any symbols and also at least one uppercase letter and at least one number.
            """
        )
