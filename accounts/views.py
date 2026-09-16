from smtplib import SMTPException

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.urls import reverse_lazy
from django.views.generic import CreateView, UpdateView

from accounts.form import UserLoginForm, UserRegistrationForm, UserProfileForm
from accounts.models import User
from config import settings


# Create your views here.

class SignIn(LoginView):
    template_name = "sign_in.html"
    authentication_form = UserLoginForm
    redirect_authenticated_user = True


class Register(CreateView):
    template_name = "register.html"
    form_class = UserRegistrationForm
    model = User
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        response = super().form_valid(form)

        try:
            sent_count = send_mail(
                subject="Добро пожаловать в SkyStore!",
                message=(
                    "Вы успешно зарегистрировались в SkyStore.\n"
                    "Теперь вы можете войти, используя свою почту и пароль."
                ),
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[self.object.email],
                fail_silently=False,
            )
        except (SMTPException, OSError):
            sent_count = 0

        if sent_count:
            messages.success(
                self.request,
                "Аккаунт создан. Письмо отправлено на вашу почту.",
            )
        else:
            messages.warning(
                self.request,
                "Аккаунт создан, но письмо отправить не удалось. "
                "Вы можете войти.",
            )

        return response


class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "profile.html"
    success_url = reverse_lazy("profile")
    success_message = "Изменения профиля сохранены."

    def get_object(self, queryset=None):
        return self.request.user
