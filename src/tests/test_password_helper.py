from unittest import TestCase

from utilise.password_helper import PasswordHelper

__author__ = 'James Stidard'


class TestPasswordHelper(TestCase):

    def old_validator(self, stored_password, guessed_password):
        return stored_password == guessed_password

    def test_create_password(self):
        new_password = 'my new shiney password'
        # result = PasswordHelper.create_password(new_password)
        # print(result)
