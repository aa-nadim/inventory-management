from django.test import TestCase
from properties.forms import SignUpForm
from django.contrib.auth.models import User

class SignUpFormTest(TestCase):
    def test_form_valid_data(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password',
            'confirm_password': 'password'
        }
        form = SignUpForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_form_invalid_password_mismatch(self):
        form_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'password',
            'confirm_password': 'differentpassword'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        # Check for non-field errors instead of field-specific errors
        self.assertTrue(form.non_field_errors())  # Check if there are non-field errors
        self.assertIn("Passwords do not match.", form.non_field_errors())

    def test_form_invalid_email(self):
        form_data = {
            'username': 'testuser',
            'email': 'invalidemail',
            'password': 'password',
            'confirm_password': 'password'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('email' in form.errors)
        self.assertEqual(form.errors['email'], ['Enter a valid email address.'])

    def test_form_username_already_taken(self):
        # Create a user to check if username validation works
        User.objects.create_user(username="existinguser", password="password", email="existinguser@example.com")
        form_data = {
            'username': 'existinguser',
            'email': 'newuser@example.com',
            'password': 'password',
            'confirm_password': 'password'
        }
        form = SignUpForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertTrue('username' in form.errors)
        self.assertEqual(form.errors['username'], ['This username is already taken.'])
