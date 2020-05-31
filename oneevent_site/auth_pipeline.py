from django.shortcuts import redirect
from django.contrib import messages


def enforce_email(request, details, user, *args, **kwargs):
    email = None
    if user is not None:
        email = user.email

    if not email:
        email = details.get('email')

    if not email:
        messages.error(
            request,
            "The authentication provider did not provide a verified email address. "
            "Please make sure it is configured and verified in the provider's settings page.",
        )
        return redirect("login")
