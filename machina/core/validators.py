from django.core import validators
from django.core.exceptions import ImproperlyConfigured
from django.utils.deconstruct import deconstructible
from django.utils.encoding import smart_str
from django.utils.translation import gettext_lazy as _

from machina.conf import settings as machina_settings


class NullableMaxLengthValidator(validators.MaxLengthValidator):
    """ Provides a way to not validate an input if the max length is None """

    def __call__(self, value):
        if self.limit_value is None:
            # If the limit value is None, this means that there is no
            # limit value at all. The default validation process is not
            # performed.
            return
        super().__call__(value)


@deconstructible
class MarkupMaxLengthValidator:
    """
    Validates the max length of an input written in the markup language defined in the settings.

    This is a proxy that use the implementation defined in MACHINA_MARKUP_MAX_LENGTH_VALIDATOR
    setting.
    """

    def __init__(self, limit_value):
        self.validator = self._get_markup_maxlength_validator(limit_value)

    def __call__(self, value):
        self.validator(value)

    @staticmethod
    def _get_markup_maxlength_validator(max_length):
        dotted_path = machina_settings.MARKUP_MAX_LENGTH_VALIDATOR
        try:
            module, validator = dotted_path.rsplit('.', 1)
            module, validator = smart_str(module), smart_str(validator)
            validator = getattr(__import__(module, {}, {}, [validator]), validator)
            return validator(max_length)
        except ImportError as e:
            raise ImproperlyConfigured(
                _('Could not import MARKUP_MAX_LENGTH_VALIDATOR {}: {}').format(
                    machina_settings.MARKUP_MAX_LENGTH_VALIDATOR, e
                )
            )
