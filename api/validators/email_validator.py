from rest_framework.exceptions import ValidationError
from django.utils.translation import gettext as _


def validate_local_name(
        local_name: str,
        min_length=2,
        max_length=50,
        allowed_characters="!=#$%&';+-.?^_{}`~"
) -> None:
    """
        Local name is the first part in email (before @).
        It must consist of only:
        - english letters (lower or upper case);
        - digits;
        - allowed characters.
        Length should be from min_length to max_length

    """
    if not min_length <= len(local_name) <= max_length:
        raise ValidationError(_("Email local name length must be from %(min_length)d to %(max_length)d." % {"max_length": max_length, "min_length": min_length}))
    for item in local_name.lower():
        if 48 <= ord(item) <= 57 or  97 <= ord(item) <= 122 or item in allowed_characters:
            continue
        raise ValidationError(_("Email contains invalid characters."))


def validate_domain(
        domain: str,
        min_length_first_part=2,
        max_length_first_part=20,
        min_length_second_part=2,
        max_length_second_part=7,
) -> None:
    """
        Domain name is the second part in email (after @).
        It must consist of only:
        - english letters (lower or upper case);
        - digits;
        - "-" or ".".
        Domain name must not end with "-".
        Length of two parts of domainname should be from min_length to max_length

    """
    domain_list= domain.split(".")
    if len(domain_list) != 2 or domain.endswith("-"):
        raise ValidationError(_("Invalid domain name."))
    if not min_length_first_part <= len(domain_list[0]) <= max_length_first_part:
        raise ValidationError(_("Invalid domain name length."))
    if not min_length_second_part <= len(domain_list[1]) <= max_length_second_part:
        raise ValidationError(_("Invalid domain name length."))
    for item in domain.lower():
        if ord(item) < 48 or 57 < ord(item) < 97 or ord(item) > 122:
            if item  in ("-", "."):
                continue
            raise ValidationError(_("Domain name contains invalid characters."))


def validate_user_email(email: str) -> None:
    email_list = email.split("@")
    if len(email_list) != 2:
        raise ValidationError(_("Invalid email."))
    validate_local_name(email_list[0])
    validate_domain(email_list[1])
