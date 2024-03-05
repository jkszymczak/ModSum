from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.views import View

# Create your views here.

class ShopMainPage(View):
    template_name = 'shop/index.html'

    def get(self, request, *args, **kwargs):

        if not request.user.is_authenticated:
            return redirect('/login')

        return render(request, self.template_name)
