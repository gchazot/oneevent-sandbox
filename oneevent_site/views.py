from django.contrib import messages
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.shortcuts import redirect, render
from django.contrib.auth.views import login_required
from django.views.decorators.http import require_POST
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset, Layout, Fieldset, Field
from social_django.views import disconnect
from social_core.exceptions import NotAllowedToDisconnect


class UserDetailsForm(ModelForm):
    class Meta:
        fields = ("first_name", "last_name", "email")
        model = User

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_method = "post"
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
        return render(request, "oneevent_sandbox/user_profile.html", {"user_form": user_form})


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
