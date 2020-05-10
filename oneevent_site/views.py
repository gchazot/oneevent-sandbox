from django.contrib import messages
from django.shortcuts import redirect, render


def user_profile(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please login to see your profile")
        return redirect("login")
    else:
        return render(request, "oneevent_sandbox/user_profile.html")
