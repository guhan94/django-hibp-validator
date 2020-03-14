import requests
import hashlib
import logging

from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class HIBPCheck(object):
    def __init__(self):
        self.hibp_api_endpoint = 'https://api.pwnedpasswords.com/range/'

    @staticmethod
    def hash_password(password: str) -> str:
        hash_val = hashlib.sha1(password.encode('utf-8'))
        return hash_val.hexdigest().__str__()

    def _get_password_range(self, hash_index: str):
        try:
            # Querying HIBP for a range of password hashes by k-Anonymity model.
            response = requests.get(f'{self.hibp_api_endpoint}{hash_index}', headers={'Add-Padding': 'true'})
            if response.status_code == 200:
                return response.text
            else:
                return None
        except requests.exceptions.RequestException as e:
            logging.error(f'Something went wrong while querying HIBP: {e}')
            raise e

    def is_pwned(self, passwd_hash: str) -> bool:
        index = passwd_hash[0:5].upper()
        hash_list = self._get_password_range(hash_index=index).splitlines()
        for hash in hash_list:
            hash = index + hash
            hash, count = hash.split(':')
            if passwd_hash.upper() == hash and int(count) > 0:
                # Oops given password is indeed pwned!
                return True
        # No hash matches found for the given password hash
        return False

    def validate(self, password, user=None):
        if self.is_pwned(passwd_hash=self.hash_password(password)):
            raise ValidationError(
                _("This password was found to be part of a breach according to haveibeenpwned.com"),
                code='password_compromised',
            )

    def get_help_text(self):
        return _(
            "Your password would be validated against 'Have I Been Pwned'"
        )
