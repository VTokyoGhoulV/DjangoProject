from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from accounts.models import User


class UserRegistrationForm(UserCreationForm):

    class Meta:
        model = User
        fields = ["email", "avatar", "mobile_number", "country"]
        labels = {
            "email": "Почта",
            "avatar": "Аватар профиля",
            "mobile_number": "Номер мобильного телефона",
            "country": "Страна проживания",
        }
        widgets = {
            "avatar": forms.FileInput(
                attrs={
                    "class": "form-control",
                    "accept": "image/*",
                }
            ),
        }

    def clean_email(self):
        email = self.cleaned_data["email"]

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Email already registered")

        return email


class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label="Почта",
        widget=forms.EmailInput(attrs={"class": "form-control"}),
    )
    password = forms.CharField(
        label="Пароль",
        strip=False,
        widget=forms.PasswordInput(
            attrs={
                "class": "form-control",
                "autocomplete": "current-password",
            }
        ),
    )

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["email", "avatar", "mobile_number", "country"]
        labels = {
            "email": "Почта",
            "avatar": "Аватар профиля",
            "mobile_number": "Номер телефона",
            "country": "Страна",
        }
        widgets = {
            "avatar": forms.FileInput(
                attrs={"accept": "image/*"}
            ),
        }
        error_messages = {
            "email": {
                "unique": "Эта почта уже используется другим пользователем.",
            },
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for field in self.fields.values():
            field.widget.attrs["class"] = "form-control"