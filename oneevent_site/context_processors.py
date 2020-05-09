def social_auth_extra_data(request):
    social = _get_prefered_social(request.user)

    if social is not None:
        return {
            'user_avatar_url': social.extra_data.get('user_avatar'),
        }
    return {}


def _get_prefered_social(user):
    if user and user.is_authenticated:
        for provider in ('google-oauth2', 'github'):
            try:
                return user.social_auth.get(provider=provider)
            except user.social_auth.DoesNotExist:
                continue
