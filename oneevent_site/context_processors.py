def social_auth_extra_data(request):
    social = _get_prefered_social(request.user)

    if social is None:
        return {}

    return {
        'user_avatar_url': social.extra_data.get('user_avatar', ''),
    }


def _get_prefered_social(user):
    if user and user.is_authenticated:
        for provider in ('google-oauth2', 'github', 'facebook'):
            try:
                return user.social_auth.filter(provider=provider)[0]
            except IndexError:
                continue
