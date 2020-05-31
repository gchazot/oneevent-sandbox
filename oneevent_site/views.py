from django.contrib import messages
from django.contrib.auth.models import User
from django.templatetags.static import static
from django.forms import Form, ModelForm
from django.shortcuts import redirect, render, reverse
from django.contrib.auth.views import login_required
from django.views.decorators.http import require_POST
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset, Layout, Fieldset, Field, HTML, Hidden
from social_django.views import disconnect
from social_core.exceptions import NotAllowedToDisconnect


class UserDetailsForm(ModelForm):
    class Meta:
        fields = ("first_name", "last_name", "email")
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_action = "user_profile"

        self.helper.layout = Layout(
            Fieldset(
                None,
                *(Field(field_name) for field_name in self.Meta.fields),
            ),
            FormActions(
                Submit("save", "Save", css_class="btn btn-success"),
                Reset("reset", "Reset", css_class="btn btn-warning"),
            ),
        )


class UserSocialAuthDisconnectForm(Form):
    def __init__(self, social_auth, *args, **kwargs):
        super().__init__(*args, **kwargs)

        provider = social_auth.provider

        self.helper = FormHelper()
        self.helper.form_action = reverse("user_disconnect_social_auth",
                                          kwargs={"backend": provider})

        self.helper.layout = Layout(
            HTML(f'<img src="{get_social_auth_icon_url(provider)}"/>'),
            Hidden(name='next', value=reverse("user_profile")),
            HTML(f"<span>{get_social_auth_display_name(provider)} </span>"),
            HTML('(<button type="submit" class="btn btn-link"'
                 'style="padding: 0; border: 0;">disconnect account</button>)'),
        )


def get_social_auth_display_name(social_auth):
    return {
        'github': 'Github',
        'google-oauth2': 'Google',
        'facebook': 'Facebook',
    }.get(social_auth)


def get_social_auth_icon_url(social_auth):
    icon_name = {
        'github': 'github',
        "google-oauth2": "google",
        'facebook': 'facebook',
    }.get(social_auth)
    return static(f"social_provider_icons/{icon_name}.png")


@login_required
def user_profile(request):
    if not request.user.is_authenticated:
        messages.info(request, "Please login to see your profile")
        return redirect("login")
    else:
        user_form = UserDetailsForm(request.POST or None, instance=request.user)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, "User details saved")
        elif user_form.is_bound:
            messages.error(request, "Please correct errors below")

        disconnect_forms = [
            UserSocialAuthDisconnectForm(social_auth)
            for social_auth in request.user.social_auth.all()
        ]

        return render(request, "oneevent_sandbox/user_profile.html",
                      {"user_form": user_form, "disconnect_forms": disconnect_forms})


@login_required
@require_POST
def user_disconnect_social_auth(request, backend):
    try:
        response = disconnect(request, backend)
        messages.success(request, f"Account unlinked successfully")
        return response
    except NotAllowedToDisconnect:
        messages.error(request, "You can not disconnect from the last social provider")
        return redirect("user_profile")
