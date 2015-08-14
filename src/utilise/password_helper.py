__author__ = 'James Stidard'

import hashlib
import os
import base64


class PasswordHelper:

    ALGORITHM  = 'sha512'
    HASH_BYTES = 64
    ITERATIONS = 10000
    SALT_BYTES = HASH_BYTES

    ALGORITHM_INDEX = 0
    ITERATION_INDEX = 1
    SALT_INDEX = 2
    HASH_INDEX = 3
    PART_COUNT = 4
    DELIMITER  = ';'

    @staticmethod
    def create_password(password='', salt=None):
        algorithm  = PasswordHelper.ALGORITHM
        iterations = PasswordHelper.ITERATIONS
        salt       = os.urandom(PasswordHelper.SALT_BYTES) if not salt else salt
        salt_bytes = PasswordHelper.SALT_BYTES
        password   = password.encode()
        delimiter  = PasswordHelper.DELIMITER

        if len(salt) != salt_bytes:
            raise Exception('The provided salt does not meet the required salt length (in bytes) of the current ' +
                            'stratagem. Provided: ' + str(len(salt)) + '. Required: ' + str(salt_bytes))

        password_hash = hashlib.pbkdf2_hmac(algorithm, password, salt, iterations)

        # Convert the hash and salt into their base64 string representation
        password_hash = base64.b64encode(password_hash).decode()
        salt          = base64.b64encode(salt).decode()

        return algorithm + delimiter + str(iterations) + delimiter + str(salt) + delimiter + password_hash

    @staticmethod
    def validate_password(stored_password='', guessed_password='', update_stratagem=True, legacy_validator=None):
        # If legacy validator, try that first. and then update to new stratagem if they want.
        if legacy_validator and legacy_validator(stored_password, guessed_password):
            if update_stratagem: return PasswordHelper.create_password(guessed_password)
            else: return True

        delimiter        = PasswordHelper.DELIMITER
        algorithm_index  = PasswordHelper.ALGORITHM_INDEX
        iteration_index  = PasswordHelper.ITERATION_INDEX
        salt_index       = PasswordHelper.SALT_INDEX
        hash_index       = PasswordHelper.HASH_INDEX
        part_count       = PasswordHelper.PART_COUNT

        # Split the stored password around the set delimiter
        parts = stored_password.split(delimiter)

        # If not the number of parts we expect return false (Invalid, legacy, password guess or corrupt data)
        if len(parts) != part_count: return False

        # Get the hash and the PBKDF2 parameters from parts
        algorithm     = parts[algorithm_index]
        iterations    = int( parts[iteration_index] )
        salt          = base64.b64decode( parts[salt_index] )
        password_hash = base64.b64decode( parts[hash_index] )

        # If anything's looking wrong at this point get out.
        # TODO: Best log this (should never be hit - maybe exception)
        if algorithm not in hashlib.algorithms_available or iterations == 0: return False

        # Give the guess a shot with the parameters used on the stored hash
        guess_hash = hashlib.pbkdf2_hmac(algorithm, guessed_password.encode(), salt, iterations)

        correct_guess      = PasswordHelper._slow_equals(guess_hash, password_hash)
        outdated_stratagem = algorithm          != PasswordHelper.ALGORITHM  or \
                             iterations         != PasswordHelper.ITERATIONS or \
                             len(salt)          != PasswordHelper.SALT_BYTES or \
                             len(password_hash) != PasswordHelper.HASH_BYTES

        # Return the new password blob to store if update is required and guess was correct
        if correct_guess and update_stratagem and outdated_stratagem:
            return PasswordHelper.create_password(guessed_password)

        return correct_guess

    @staticmethod
    def change_password(stored_password, old_password, new_password, salt=None):
        if PasswordHelper.validate_password(stored_password, old_password, False):
            return PasswordHelper.create_password(new_password, salt)

        return False

    @staticmethod
    def _slow_equals(a, b):
        diff, i = len(a) ^ len(b), 0
        while i < len(a) and i < len(b):
            diff |= a[i] ^ b[i]
            i    += 1
        return diff == 0
