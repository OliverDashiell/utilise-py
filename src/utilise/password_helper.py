__author__ = 'James Stidard'

import hashlib
import os
import base64
from collections import namedtuple


class PasswordHelper:

    Result = namedtuple('Result', ['success', 'new_password'])
    _Parts = namedtuple('Parts', ['algorithm', 'iterations', 'salt', 'hash'])

    algorithm  = 'sha512'
    hash_bytes = 64
    iterations = 10000
    salt_bytes = hash_bytes

    _ALGORITHM_INDEX = 0
    _ITERATION_INDEX = 1
    _SALT_INDEX = 2
    _HASH_INDEX = 3
    _PART_COUNT = 4
    _DELIMITER  = ';'

    @staticmethod
    def create_password(password: str, salt: bytes=None) -> str:
        self = PasswordHelper
        salt = os.urandom(self.salt_bytes) if not salt else salt

        if len(salt) != self.salt_bytes:
            raise Exception('The provided salt does not meet the required salt length (in bytes) of the current '
                            'stratagem. Provided: ' + str(len(salt)) + '. Required: ' + str(self.salt_bytes))

        password_hash = hashlib.pbkdf2_hmac(self.algorithm, password.encode(), salt, self.iterations)

        # Convert the hash and salt into their base64 string representation
        password_hash = base64.b64encode(password_hash).decode()
        salt          = base64.b64encode(salt).decode()
        delimiter     = self._DELIMITER

        return delimiter.join( [self.algorithm, str(self.iterations), str(salt), password_hash] )

    @staticmethod
    def validate_password(stored_password: str,
                          guessed_password: str,
                          update_stratagem: bool=True,
                          legacy_validator=None) -> (bool, str):

        # TODO: Type hint for legacy function on release of python 3.5
        self = PasswordHelper

        # If legacy validator, try that first. and then update to new stratagem if they want.
        if legacy_validator and legacy_validator(stored_password, guessed_password):
            new_password = self.create_password(guessed_password) if update_stratagem else ''
            return self.Result(True, new_password)

        parts = self._parts_from_password(stored_password)

        # If no parts return false (A invalid legacy password guess or corrupt data)
        if not parts: return self.Result(False, '')

        # Give the guess a shot with the parameters used on the stored hash
        guess_hash = hashlib.pbkdf2_hmac(parts.algorithm, guessed_password.encode(), parts.salt, parts.iterations)

        correct_guess      = self._slow_equals(guess_hash, parts.hash)
        outdated_stratagem = parts.algorithm  != self.algorithm  or \
                             parts.iterations != self.iterations or \
                             len(parts.salt)  != self.salt_bytes or \
                             len(parts.hash)  != self.hash_bytes

        # Return the new password blob to store if update is required and guess was correct
        password_required = correct_guess and update_stratagem and outdated_stratagem
        new_password      = self.create_password(guessed_password) if password_required else ''

        return self.Result(correct_guess, new_password)

    @staticmethod
    def change_password(stored_password: str,
                        old_password: str,
                        new_password: str,
                        salt: bytes=None,
                        legacy_validator=None) -> (bool, str):

        if PasswordHelper.validate_password(stored_password, old_password, False, legacy_validator).success:
            new_password = PasswordHelper.create_password(new_password, salt)
            return PasswordHelper.Result(True, new_password)

        return PasswordHelper.Result(False, '')

    @staticmethod
    def _parts_from_password(password: str) -> (str, int, str, str):
        self  = PasswordHelper
        parts = password.split(self._DELIMITER)

        # If not the number of parts we expect return false (A invalid legacy password guess or corrupt data)
        if len(parts) != self._PART_COUNT: return

        # Get the hash and the PBKDF2 parameters from parts
        algorithm     = parts[self._ALGORITHM_INDEX]
        iterations    = int( parts[self._ITERATION_INDEX] )
        salt          = base64.b64decode( parts[self._SALT_INDEX] )
        password_hash = base64.b64decode( parts[self._HASH_INDEX] )

        # If anything's looking wrong at this point get out.
        if algorithm not in hashlib.algorithms_available:
            raise Exception(algorithm + ' is not available to the hashlib module on this system. '
                            'See hashlib.algorithms_available.')
        elif iterations <= 0:
            raise Exception('A iteration count of ' + str(iterations) + ' was parsed from ' +
                            parts[self._ITERATION_INDEX] + '. An iteration count of 1, or higher, is required.')

        return self._Parts(algorithm=algorithm, iterations=iterations, salt=salt, hash=password_hash)

    @staticmethod
    def _slow_equals(a, b) -> bool:
        diff, i = len(a) ^ len(b), 0
        while i < len(a) and i < len(b):
            diff |= a[i] ^ b[i]
            i    += 1
        return diff == 0
