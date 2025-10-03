from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .forms import UserRegistrationForm, ProfileForm
from .models import Profile
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from accounts.models import Profile

def register(request):
    if request.method == 'POST':
        uform = UserRegistrationForm(request.POST)
        pform = ProfileForm(request.POST, request.FILES)
        if uform.is_valid() and pform.is_valid():
            user = uform.save(commit=False)
            user.set_password(uform.cleaned_data['password'])
            user.save()

            # create or get profile to avoid UNIQUE constraint error
            profile, created = Profile.objects.get_or_create(user=user)
            profile.is_employer = 'is_employer' in request.POST and request.POST.get('is_employer') == 'on'
            
            # update other fields from the form
            for field in pform.cleaned_data:
                setattr(profile, field, pform.cleaned_data[field])

            profile.save()
            messages.success(request, "Account created. Please login.")
            return redirect('login')
    else:
        uform = UserRegistrationForm()
        pform = ProfileForm()
    
    return render(request, 'accounts/register.html', {'uform': uform, 'pform': pform})


def user_login(request):
    if request.method == 'POST':
        uname = request.POST.get('username')
        pwd = request.POST.get('password')
        user = authenticate(username=uname, password=pwd)
        if user:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'accounts/login.html', {'error': 'Invalid credentials'})
    return render(request, 'accounts/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    profile = Profile.objects.get(user=request.user)
    if request.method == 'POST':
        pform = ProfileForm(request.POST, request.FILES, instance=profile)
        if pform.is_valid():
            pform.save()
            return redirect('profile')
    else:
        pform = ProfileForm(instance=profile)
    return render(request, 'accounts/profile.html', {'pform': pform, 'profile': profile})

