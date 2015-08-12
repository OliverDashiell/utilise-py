__author__ = 'James Stidard'

import hashlib
import os
import base64


class PasswordHelper:

    ALGORITHM  = 'sha512'
    ITERATIONS = 10000
    HASH_BYTES = 64
    SALT_BYTES = HASH_BYTES

    ALGORITHM_INDEX = 0
    ITERATION_INDEX = 1
    SALT_INDEX = 2
    HASH_INDEX = 3
    PART_COUNT = 4
    DELIMITER  = ';'

    @staticmethod
    def create_password(password='', salt=None):
        salt = os.urandom(PasswordHelper.SALT_BYTES) if not salt else salt

        if len(salt) != PasswordHelper.SALT_BYTES:
            raise Exception('The provided salt does not meet the required salt length (in bytes) of the current ' +
                            'stratagem. Provided: ' + str(len(salt)) + '. Required: ' + str(PasswordHelper.SALT_BYTES))

        password_hash = hashlib.pbkdf2_hmac(PasswordHelper.ALGORITHM, password, salt, PasswordHelper.ITERATIONS)

        return PasswordHelper.ALGORITHM     + PasswordHelper.DELIMITER + \
            base64.b64encode(password_hash) + PasswordHelper.DELIMITER + \
            str(PasswordHelper.ITERATIONS)  + PasswordHelper.DELIMITER + \
            base64.b64encode(salt)

    @staticmethod
    def validate_password(stored_password='', guessed_password='', update_stratagem=True, legacy_validator=None):
        # If legacy validator, try that first. and then update to new stratagem if they want.
        if legacy_validator and legacy_validator(stored_password, guessed_password):
            if update_stratagem: return PasswordHelper.create_password(guessed_password)
            else: return True

        # Split the stored password around the set delimiter
        parts = stored_password.split(PasswordHelper.DELIMITER)

        # If not the number of parts we expect return false (Invalid, legacy, password guess or corrupt data)
        if len(parts) != PasswordHelper.PART_COUNT: return False

        # Get the hash and the PBKDF2 parameters from parts
        algorithm     = parts[PasswordHelper.ALGORITHM_INDEX]
        iterations    = int( parts[PasswordHelper.ITERATION_INDEX] )
        password_hash = base64.b64decode( parts[PasswordHelper.HASH_INDEX] )
        salt          = base64.b64decode( parts[PasswordHelper.SALT_INDEX] )

        # If anything's looking wrong at this point get out.
        # TODO: Best log this (should never be hit - maybe exception)
        if algorithm not in hashlib.algorithms or iterations == 0: return False

        # Give the guess a shot with the parameters used on the stored hash
        guess_hash = hashlib.pbkdf2_hmac(algorithm, guessed_password, salt, iterations)

        # TODO: Slow equals
        correct_guess      = guess_hash == password_hash
        outdated_stratagem = algorithm          != PasswordHelper.ALGORITHM  or \
                             iterations         != PasswordHelper.ITERATIONS or \
                             len(salt)          != PasswordHelper.SALT_BYTES or \
                             len(password_hash) != PasswordHelper.HASH_BYTES

        # Return the new password blob to store if update is required and guess was correct
        if correct_guess and update_stratagem and outdated_stratagem:
            return PasswordHelper.create_password(guessed_password)

        return correct_guess

    @staticmethod
    def change_password(stored_password, old_password, new_password, new_salt=None):
        if PasswordHelper.validate_password(stored_password, old_password, False):
            return PasswordHelper.create_password(new_password, new_salt)

        return False
