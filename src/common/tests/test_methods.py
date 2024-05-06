import string
from django.test import TestCase
from django.conf import settings
from common.methods import get_unique_code_chars


class TestMethods(TestCase):
    def test_get_unique_code_chars(self):
        # Set the suffix length to a known value for testing
        settings.UNIQUE_CODE_SUFFIX_LENGTH = 10

        # Generate unique code characters
        unique_code_chars = get_unique_code_chars()

        # Check if the generated code has the correct length
        self.assertEqual(len(unique_code_chars), settings.UNIQUE_CODE_SUFFIX_LENGTH)

        # Check if all characters in the code are from the alphabet
        alphabet = string.ascii_lowercase + string.digits
        self.assertTrue(all(char in alphabet for char in unique_code_chars))

        # Reset the suffix length setting to avoid affecting other tests
        delattr(settings, "UNIQUE_CODE_SUFFIX_LENGTH")
