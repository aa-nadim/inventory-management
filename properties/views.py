from django.http import HttpResponse
from django.contrib.auth.models import Group
from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import SignUpForm
import logging

logger = logging.getLogger(__name__)

def home(request):
    return HttpResponse("Welcome to the Home Page!")

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.is_active = False  # Set the user to inactive until admin activates
                user.save()

                # Add the user to the "Property Owners" group
                group, created = Group.objects.get_or_create(name='Property Owners')
                user.groups.add(group)

                logger.info(f"User {user.username} created and added to Property Owners group.")
                
                messages.success(
                    request, 
                    'Your account has been created. Wait for admin activation.'
                )
                return redirect('signup_success')
            except Exception as e:
                logger.error(f"Signup error for user {request.POST.get('username')}: {e}")
                messages.error(
                    request, 
                    'An unexpected error occurred during signup. Please try again later.'
                )
        else:
            messages.error(
                request, 
                'Error during sign-up. Please fix the errors below.'
            )
    else:
        form = SignUpForm()
    
    return render(request, 'signup.html', {'form': form})

def signup_success(request):
    """
    View for displaying a success message after the user signs up.
    """
    return render(request, 'signup_success.html')
