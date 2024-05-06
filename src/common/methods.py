import random
import string

from django.conf import settings

import logging


logger = logging.getLogger(__name__)


def get_unique_code_chars():
    """
    Generates the generic part of a unique code by default, 8 characters that are a random mix of
    lowercase letters and digits. It can't include the prefix part because, when used as the model
    field default, it doesn't know anything about the object or model it's operating on.

    :return: The characters to initially/ temporarily set as the default value for a Global ID
    """

    length = getattr(settings, "UNIQUE_CODE_SUFFIX_LENGTH", None)

    if length:
        # if the setting exists is must be a number > 8
        try:
            length = int(length)
            if length < 8 or length > 12:
                raise Exception
        except Exception:
            # this is broad on purpose.  Any misconfiguration should result in a None length,
            # regardless if it was a number not in the (8, 12) range or a non-integer setting
            length = None
            logger.warn(
                "Improperly configured Unique Code length. Must be an integer between 8 and 12."
            )

    if not length:
        # there is no setting defined or the setting is misconfigured, default to 8
        length = 8

    alphabet = string.ascii_lowercase + string.digits
    code_chars = "".join(random.choices(alphabet, k=length))

    return code_chars
