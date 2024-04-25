from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from .models import UserProfile, create_profile
from .forms import UserProfileForm

def register(response):

    if response.method == "POST":
        form = UserCreationForm(response.POST)
        if form.is_valid():
            form.save()
            create_profile(response, response.user, True)
            return redirect("/")
    else:
        form = UserCreationForm()
    return render(response, "register/register.html", {"form": form})

@login_required
def account(response):
    if response.method == "POST":
        profile = UserProfile.objects.get(user=response.user)
        profile_form = UserProfileForm(response.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()

    else:
        profile = UserProfile.objects.get(user=response.user)
        profile_form = UserProfileForm(instance=profile)
    return render(response, "account/account.html", {'profile_form': profile_form})

