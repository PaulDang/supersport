from django import forms
from .models import User


class RegisterForm(forms.ModelForm):
    firstName = forms.CharField(required=True)
    phone = forms.CharField(required=True)
    username = forms.CharField(required=True)
    email = forms.EmailField(required=True)
    password = forms.PasswordInput()

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


class UpdatedForm(forms.ModelForm):
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

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].disabled = True
        self.fields["password"].disabled = True

    def save(self, commit=True):
        user = super(UpdatedForm, self).save(commit=False)
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
