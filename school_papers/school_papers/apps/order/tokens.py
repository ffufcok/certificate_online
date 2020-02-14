from django.contrib.auth.tokens import PasswordResetTokenGenerator
import six
from random import getrandbits


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
                six.text_type(user.pk) + six.text_type(timestamp) +
                six.text_type(user.is_active) + str(getrandbits(20))
        )


email_token = TokenGenerator()