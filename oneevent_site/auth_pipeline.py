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
    elif user and not user.email:
       user.email = email
       user.save()


def facebook_avatar_url(social, backend, *args, **kwargs):
    if backend.name == 'facebook':
        facebook_id = social.extra_data['id']
        avatar_url = f'http://graph.facebook.com/{facebook_id}/picture?type=small'
        social.extra_data['user_avatar'] = avatar_url
        social.save()
