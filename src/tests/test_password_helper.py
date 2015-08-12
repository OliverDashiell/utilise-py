__author__ = 'James Stidard'

from unittest import TestCase

from utilise.password_helper import PasswordHelper


class TestPasswordHelper(TestCase):

    def old_validator(self, stored_password, guessed_password):
        return stored_password == guessed_password

    def test_create_password(self):
        new_password = 'my new shiny password'
        result       = PasswordHelper.create_password(new_password)
        self.assertIsNotNone(result, 'password was not able to be created')

    def test_valid_password(self):
        new_password    = 'my new shiny password'
        stored_password = PasswordHelper.create_password(new_password)
        guess_password  = 'my new shiny password'
        self.assertTrue(PasswordHelper.validate_password(stored_password, guess_password), 'Correct password not valid')

    def test_invalid_password(self):
        new_password    = 'my new shiny password'
        stored_password = PasswordHelper.create_password(new_password)
        guess_password  = 'my-new-shiny-password'
        self.assertFalse(PasswordHelper.validate_password(stored_password, guess_password),
                         'Incorrect password was found valid')

    def test_change_password_fail(self):
        actual_password    = 'my cruddy old password'
        stored_password    = PasswordHelper.create_password(actual_password)
        incorrect_password = 'my typ0'
        new_password       = 'my new shiny password'
        result             = PasswordHelper.change_password(stored_password, incorrect_password, new_password)
        self.assertFalse(result)

    def test_change_password_success(self):
        old_password       = 'my cruddy old password'
        stored_password    = PasswordHelper.create_password(old_password)
        new_password       = 'my new shiny password'
        result             = PasswordHelper.change_password(stored_password, old_password, new_password)
        self.assertIsNotNone(result)
        self.assertIsInstance(result, str, 'New password to store after changing password not returned')

    # TODO: update strategem tests

    # TODO: test passing in a salt

    # TODO: test updated passwords are returned correctly

    # TODO: test legacy validator
    def test_correct_legacy_password(self):
        new_password    = 'my new shiny password'
        guess_password  = 'my new shiny password'
        old_comparator  = lambda a, b: a == b
        self.assertTrue(PasswordHelper.validate_password(new_password, guess_password, legacy_validator=old_comparator),
                        'Correct password not valid')

    def test_correct_current_password(self):
        new_password    = 'my new shiny password'
        stored_password = PasswordHelper.create_password(new_password)
        guess_password  = 'my new shiny password'
        old_comparator  = lambda a, b: a == b
        result          = PasswordHelper.validate_password(stored_password, guess_password,
                                                           legacy_validator=old_comparator)
        self.assertTrue(result, 'Correct password not valid')

    def test_incorrect_legacy_password(self):
        new_password    = 'my new shiny password'
        guess_password  = 'my-new-shiny-password'
        old_comparator  = lambda a, b: a == b
        result          = PasswordHelper.validate_password(new_password, guess_password,
                                                           legacy_validator=old_comparator)
        self.assertFalse(result, 'Correct password not valid')

    def test_incorrect_current_password(self):
        new_password    = 'my new shiny password'
        stored_password = PasswordHelper.create_password(new_password)
        guess_password  = 'my-new-shiny-password'
        old_comparator  = lambda a, b: a == b
        result          = PasswordHelper.validate_password(stored_password, guess_password,
                                                           legacy_validator=old_comparator)
        self.assertFalse(result, 'Correct password not valid')
