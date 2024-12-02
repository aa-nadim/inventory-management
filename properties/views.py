from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm

def home(request):
    return HttpResponse("Welcome to the Home Page!")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Set the user to inactive
            user.save()
            # Add user to "Property Owners" group
            group, _ = Group.objects.get_or_create(name='Property Owners')
            user.groups.add(group)
            user.save()

            messages.success(request, 'Your account has been created. Wait for admin activation.')
            return redirect('signup_success')
        else:
            messages.error(request, 'Error during sign-up. Please try again.')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})


def signup_success(request):
    """
    View for displaying a success message after the user signs up.
    """
    return render(request, 'signup_success.html')

