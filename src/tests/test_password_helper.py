__author__ = 'James Stidard'

from unittest import TestCase

from utilise.password_helper import PasswordHelper


class TestPasswordHelper(TestCase):

    def setUp(self):
        PasswordHelper.algorithm  = 'sha512'
        PasswordHelper.hash_bytes = 64
        PasswordHelper.iterations = 10000
        PasswordHelper.salt_bytes = 64

        PasswordHelper._ALGORITHM_INDEX = 0
        PasswordHelper._ITERATION_INDEX = 1
        PasswordHelper._SALT_INDEX = 2
        PasswordHelper._HASH_INDEX = 3
        PasswordHelper._PART_COUNT = 4
        PasswordHelper._DELIMITER  = ';'

    def test_create_password(self):
        new_password = 'my new shiny password'
        result       = PasswordHelper.create_password(new_password)

        self.assertIsNotNone(result, 'password was not able to be created')

    def test_valid_password(self):
        new_password    = 'my new shiny password'
        stored_password = PasswordHelper.create_password(new_password)
        guess_password  = 'my new shiny password'
        result          = PasswordHelper.validate_password(stored_password, guess_password)

        self.assertTrue(result.success, 'Correct password not valid')
        self.assertFalse(result.new_password, 'No new password should be needed')

    def test_invalid_password(self):
        new_password    = 'my new shiny password'
        stored_password = PasswordHelper.create_password(new_password)
        guess_password  = 'my-new-shiny-password'
        result          = PasswordHelper.validate_password(stored_password, guess_password)

        self.assertFalse(result.success, 'Incorrect password was found valid')
        self.assertFalse(result.new_password, 'No new password should be needed')

    def test_change_password_fail(self):
        actual_password    = 'my cruddy old password'
        stored_password    = PasswordHelper.create_password(actual_password)
        incorrect_password = 'my typ0'
        new_password       = 'my new shiny password'
        result             = PasswordHelper.change_password(stored_password, incorrect_password, new_password)

        self.assertFalse(result.success)
        self.assertFalse(result.new_password, 'No new password should be needed')

    def test_change_password_success(self):
        old_password       = 'my cruddy old password'
        stored_password    = PasswordHelper.create_password(old_password)
        new_password       = 'my new shiny password'
        result             = PasswordHelper.change_password(stored_password, old_password, new_password)

        self.assertTrue(result.success)
        self.assertIsInstance(result.new_password, str, 'New password to store after changing password not returned')
        self.assertTrue(result.new_password, 'New password not returned')

    # TODO: update stratagem tests
    def test_change_algorithm(self):
        new_algorithm            = 'sha256'
        PasswordHelper.algorithm = new_algorithm
        result                   = PasswordHelper.create_password('my shiny password')

        self.assertTrue(PasswordHelper.algorithm == 'sha256', 'Algorithm change did not stick')
        self.assertTrue(result[:len(new_algorithm)] == new_algorithm, 'new algorithm not used to hash')

    # TODO: test passing in a salt

    # TODO: test updated passwords are returned correctly

    # TODO: test legacy validator

    def test_correct_legacy_password(self):
        new_password   = 'my new shiny password'
        guess_password = 'my new shiny password'

        def old_comparator(a, b):
            return a == b

        result = PasswordHelper.validate_password(new_password, guess_password, legacy_validator=old_comparator)

        self.assertTrue(result.success, 'Correct password not valid')
        self.assertTrue(result.new_password, 'Upgrade to legacy password not supplied')

    def test_correct_current_password(self):
        new_password    = 'my new shiny password'
        stored_password = PasswordHelper.create_password(new_password)
        guess_password  = 'my new shiny password'
        old_comparator  = lambda a, b: a == b
        result          = PasswordHelper.validate_password(stored_password, guess_password,
                                                           legacy_validator=old_comparator)
        self.assertTrue(result.success, 'Correct password not valid')
        self.assertFalse(result.new_password, 'No new password should be needed')

    def test_incorrect_legacy_password(self):
        new_password    = 'my new shiny password'
        guess_password  = 'my-new-shiny-password'
        old_comparator  = lambda a, b: a == b
        result          = PasswordHelper.validate_password(new_password, guess_password,
                                                           legacy_validator=old_comparator)
        self.assertFalse(result.success, 'Correct password not valid')
        self.assertFalse(result.new_password, 'No new password should be needed')

    def test_incorrect_current_password(self):
        new_password    = 'my new shiny password'
        stored_password = PasswordHelper.create_password(new_password)
        guess_password  = 'my-new-shiny-password'
        old_comparator  = lambda a, b: a == b
        result          = PasswordHelper.validate_password(stored_password, guess_password,
                                                           legacy_validator=old_comparator)
        self.assertFalse(result.success, 'Correct password not valid')
        self.assertFalse(result.new_password, 'No new password should be needed')
