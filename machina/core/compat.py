# -*- coding: utf-8 -*-

# Standard library imports
# Third party imports
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.translation import ugettext_lazy as _

# Local application / specific library imports

# PILImage
try:
    # Try from the Pillow (or one variant of PIL) install location first.
    from PIL import Image as PILImage
except ImportError as err:  # pragma: no cover
    try:
        # If that failed, try the alternate import syntax for PIL.
        import Image as PILImage  # noqa
    except ImportError as err:
        # Neither worked, so it's likely not installed.
        raise ImproperlyConfigured(
            _("Neither Pillow nor PIL could be imported: %s") % err
        )


# Django slugify
try:
    from django.utils.text import slugify
except ImportError:  # pragma: no cover
    from django.template.defaultfilters import slugify  # noqa


# force_bytes
try:
    from django.utils.encoding import force_bytes
except ImportError:  # pragma: no cover
    from django.utils.encoding import smart_str as force_bytes  # noqa


# A settings that can be used in foreign key declarations to ensure backwards compatibility
# with Django 1.4
AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


# get_user_model
try:
    from django.contrib.auth import get_user_model
except ImportError:  # pragma: no cover
    from django.contrib.auth.models import User
    get_user_model = lambda: User
