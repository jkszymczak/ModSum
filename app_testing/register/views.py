from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views import View
from .models import UserProfile, create_profile
from .forms import UserProfileForm

class RegisterView(View):
    """This class is responsible for registering a new user."""

    def get(self, request):
        """This method is responsible for displaying the registration form.

        :param request: HttpRequest object
        :return: HttpResponse object
        """

        form = UserCreationForm()
        return render(request, "register/register.html", {"form": form})

    def post(self, request):
        """This method is responsible for registering a new user.

        :param request: HttpRequest object
        :return: HttpResponse object
        """

        form = UserCreationForm(request.POST)
        if form.is_valid():
            # form.save() # This line is commented out to break the registration process
            return redirect("/")
        return render(request, "register/register.html", {"form": form})

class AccountView(View):
    """This class is responsible for displaying the user account."""

    def post(self, request):
        """This method is responsible for updating the user account.

        :param request: HttpRequest object
        :return: HttpResponse object
        """

        if not request.user.is_authenticated:
            return redirect('/login')

        profile = get_object_or_404(UserProfile, user=request.user)
        profile_form = UserProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
        return render(request, "account/account.html", {'profile_form': profile_form})

    def get(self, request):
        """This method is responsible for displaying the user account.

        :param request: HttpRequest object
        :return: HttpResponse object
        """

        if not request.user.is_authenticated:
            return redirect('/login')

        profile = UserProfile.objects.get(user=request.user)
        profile_form = UserProfileForm(instance=profile)
        return render(request, "account/account.html", {'profile_form': profile_form})

