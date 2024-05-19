from django import forms
from .models import User
from django.core.validators import (
    RegexValidator,
    EmailValidator,
    MinLengthValidator,
    MaxLengthValidator,
)
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.forms import PasswordChangeForm


class UserFormMixin(forms.Form):
    firstName = forms.CharField(
        label=_("First name"),
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-ZÀ-Ỹà-ỹ\s]+$",
                message=_("First name chỉ nên chứa các chữ cái và dấu cách."),
                code="invalid_firstname",
            )
        ],
    )
    lastName = forms.CharField(
        label=_("Last name"),
        required=True,
        validators=[
            RegexValidator(
                regex=r"^[a-zA-ZÀ-Ỹà-ỹ\s]+$",
                message=_("Last name chỉ nên chứa các chữ cái và dấu cách."),
                code="invalid_lastname",
            )
        ],
    )
    phone = forms.CharField(
        label=_("Phone"),
        required=True,
        validators=[
            MinLengthValidator(
                10, message=_("Phone number nên có ít nhất 10 ký tự số.")
            ),
            MaxLengthValidator(
                10, message=_("Phone number nên có tối đa 10 ký tự số.")
            ),
        ],
    )
    username = forms.CharField(label=_("Username"), required=True)
    email = forms.EmailField(
        label=_("Email"),
        required=True,
        validators=[EmailValidator(message=_("Nhập địa chỉ email hợp lệ."))],
    )
    password = forms.CharField(
        label=_("Password"), widget=forms.PasswordInput(), required=True
    )
    address = forms.CharField(label=_("Address"), required=False)


class CustomAuthenticationForm(AuthenticationForm):
    error_messages = {
        "invalid_login": _(
            "Vui lòng nhập đúng %(username)s và mật khẩu. Lưu ý rằng cả hai trường đều phân biệt chữ hoa chữ thường."
        ),
        "inactive": _("Tài khoản này đang bị vô hiệu hóa."),
    }


class RegisterForm(UserFormMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = [
            "firstName",
            "lastName",
            "username",
            "email",
            "password",
            "phone",
            "address",
        ]
        widgets = {
            "password": forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super(RegisterForm, self).save(commit=False)
        user.username = self.cleaned_data["username"]
        user.password = self.cleaned_data["password"]
        user.email = self.cleaned_data["email"]
        user.firstName = self.cleaned_data["firstName"]
        user.lastName = self.cleaned_data["lastName"]
        user.phone = self.cleaned_data["phone"]
        user.address = self.cleaned_data["address"]
        if commit:
            user = User.objects.create_user(
                username=user.username,
                email=user.email,
                password=user.password,
                firstName=user.firstName,
                lastName=user.lastName,
                phone=user.phone,
                address=user.address,
            )
        return user


class UpdateUserForm(UserFormMixin, forms.ModelForm):
    username = None
    password = None

    class Meta:
        model = User
        fields = ["username", "email", "firstName", "lastName", "phone", "address"]
        exclude = ["password", "password"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].disabled = True


class MyPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(
        label="Mật khẩu cũ",
        strip=False,
        widget=forms.PasswordInput(attrs={"autofocus": True}),
    )
    new_password1 = forms.CharField(
        label="Mật khẩu mới",
        strip=False,
        widget=forms.PasswordInput,
    )
    new_password2 = forms.CharField(
        label="Nhập lại mật khẩu mới",
        strip=False,
        widget=forms.PasswordInput,
    )
