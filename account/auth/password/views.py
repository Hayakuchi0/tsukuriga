from django.contrib.auth.views import (
    PasswordChangeView, PasswordChangeDoneView,
    PasswordResetView, PasswordResetDoneView,
    PasswordResetConfirmView, PasswordResetCompleteView
)
from django.contrib.auth.mixins import LoginRequiredMixin

from ...models import User


class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    success_url = '/accounts/password/change/done'
    template_name = 'password/change.html'


class PasswordChangeDone(LoginRequiredMixin, PasswordChangeDoneView):
    template_name = 'password/done.html'


class PasswordReset(PasswordResetView):
    email_template_name = 'password/mails/message.txt'
    template_name = 'password/reset.html'
    success_url = '/account/password/reset/send'

    def form_valid(self, form):
        cleaned_email = form.cleaned_data['email']

        for user in User.objects.filter(email=cleaned_email):
            if user.has_usable_password():
                continue
            random_password = User.objects.make_random_password()
            user.set_password(random_password)
            user.save()

        return super().form_valid(form)


class PasswordResetDone(PasswordResetDoneView):
    template_name = 'password/send.html'


class PasswordResetConfirm(PasswordResetConfirmView):
    success_url = '/account/password/reset/complete'
    template_name = 'password/confirm.html'


class PasswordResetComplete(PasswordResetCompleteView):
    template_name = 'password/done.html'
