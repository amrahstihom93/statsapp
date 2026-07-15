"""
accounts/tokens.py
Email activation token generator.
Updated to use str() instead of the removed django.utils.six module.
"""
from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) +
            str(user.profile.email_confirmed)
        )


account_activation_token = AccountActivationTokenGenerator()
