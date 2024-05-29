from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .models import UserProfile, create_profile
from .forms import UserProfileForm

class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, "register/register.html", {"form": form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("/")
        return render(request, "register/register.html", {"form": form})

class AccountView(View):
    def post(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
        return render(request, "account/account.html", {'profile_form': profile_form})

    def get(self, request):
        if not request.user.is_authenticated:
            return redirect('/login')

        profile = UserProfile.objects.get(user=request.user)
        profile_form = UserProfileForm(instance=profile)
        return render(request, "account/account.html", {'profile_form': profile_form})

