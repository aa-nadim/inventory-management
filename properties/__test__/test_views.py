from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib import messages

class SignUpViewTest(TestCase):
    def test_signup_view_get(self):
        """
        Test the GET request for the signup page.
        """
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')  # Ensure the correct template is used
        self.assertContains(response, 'Sign up')  # Check if the word "Sign up" appears in the page

    def test_signup_view_post_valid(self):
        """
        Test the POST request for the signup page with valid data.
        """
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to signup_success
        self.assertRedirects(response, reverse('signup_success'))
        # Check if the user has been created in the database
        user = User.objects.get(username='newuser')
        self.assertIsNotNone(user)

    def test_signup_view_post_invalid(self):
        """
        Test the POST request for the signup page with invalid data (password mismatch).
        """
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'password123',
            'confirm_password': 'differentpassword'
        })
        self.assertEqual(response.status_code, 200)
        # Access the form from the response context and check errors
        form = response.context['form']
        self.assertTrue(form.errors)  # Check if there are form errors
        # Check for non-field errors (for password mismatch)
        self.assertIn("Passwords do not match.", form.non_field_errors())

    def test_signup_view_post_email_invalid(self):
        """
        Test the POST request for the signup page with an invalid email format.
        """
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'invalidemail',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        self.assertEqual(response.status_code, 200)
        # Access the form from the response context and check errors
        form = response.context['form']
        self.assertTrue(form.errors)  # Check if there are form errors
        self.assertIn("Enter a valid email address.", form.errors['email'])

    def test_signup_success_view(self):
        """
        Test the signup success view after a successful signup.
        """
        response = self.client.get(reverse('signup_success'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup_success.html')  # Check if the success template is used
        self.assertContains(response, 'Signup Successful')  # Check if the success message appears
