from crispy_forms.bootstrap import FormActions
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Field, Layout, HTML, Submit
from django import forms

from user.models import User


class CreateUserForm(forms.ModelForm):
    firstName = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = [
            "username",
            "email",
            "firstName",
            "lastName",
            "phone",
            "password",
            "address",
            "is_active",
            "is_staff",
            "is_superuser",
        ]
        widgets = {
            "password": forms.PasswordInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML("<div class='row'>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("firstName", css_class="input-xlarge"),
            HTML("</div>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("lastName", css_class="input-xlarge"),
            HTML("</div>"),
            HTML("</div>"),
            # --*--
            HTML("<div class='row'>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("username", css_class="input-xlarge"),
            HTML("</div>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("password", css_class="input-xlarge"),
            HTML("</div>"),
            HTML("</div>"),
            # --*--
            HTML("<div class='row'>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("email", css_class="input-xlarge"),
            HTML("</div>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("phone", css_class="input-xlarge"),
            HTML("</div>"),
            HTML("</div>"),
            # --*--
            Field("address", css_class="input-xlarge"),
            Field("is_active", css_class="form-check-inline"),
            # --*--
            HTML("<div class='row'>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("is_staff", css_class="form-check-inline"),
            HTML("</div>"),
            HTML("<div class='form-group col-md-6'>"),
            Field("is_superuser", css_class="form-check-inline"),
            HTML("</div>"),
            HTML("</div>"),
            FormActions(
                Submit("save_changes", "Tạo", css_class="btn-primary"),
            ),
        )
