from django.contrib import messages
from django.contrib.auth.models import User
from django.forms import ModelForm
from django.shortcuts import redirect, render
from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Reset, Layout, Fieldset, Field


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
