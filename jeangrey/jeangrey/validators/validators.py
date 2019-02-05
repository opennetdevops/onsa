from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

def validate_prefix(value):
    if value not in range(0,128):
        raise ValidationError(
            _('%(value)s is not a valid prefix'),
            params={'value': value},
        )