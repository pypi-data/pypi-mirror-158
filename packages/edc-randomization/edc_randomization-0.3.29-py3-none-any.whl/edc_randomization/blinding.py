from django import forms
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist
from django.utils.safestring import mark_safe

from .auth_objects import RANDO_UNBLINDED


def is_blinded_trial():
    return getattr(settings, "EDC_RANDOMIZATION_BLINDED_TRIAL", True)


def is_blinded_user(username):
    if is_blinded_trial():
        _is_blinded_user = True
        unblinded_users = getattr(settings, "EDC_RANDOMIZATION_UNBLINDED_USERS", [])
        try:
            user = get_user_model().objects.get(
                username=username, is_staff=True, is_active=True
            )
        except ObjectDoesNotExist:
            pass
        else:
            if user.username in unblinded_users:
                _is_blinded_user = False
    else:
        _is_blinded_user = False
    return _is_blinded_user


def raise_if_prohibited_from_unblinded_rando_group(username, groups):
    """A user form validation to prevent adding an unlisted
    user to the RANDO_UNBLINDED group.

    See also edc_auth's UserForm.
    """
    if RANDO_UNBLINDED in [grp.name for grp in groups] and is_blinded_user(username):
        raise forms.ValidationError(
            {
                "groups": mark_safe(
                    "This user is not unblinded and may not added "
                    "to the <U>RANDO_UNBLINDED</U> group."
                )
            }
        )
