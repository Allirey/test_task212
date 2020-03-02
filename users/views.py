from django.urls import reverse_lazy
from django.views.generic import CreateView, View
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib import messages
from django.contrib.auth import get_user_model

from .tasks import send_verification_email
from .forms import UserCreationForm
from .tokens import account_activation_token


class SignUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('activate_request')
    template_name = 'users/signup.html'

    def form_valid(self, form):
        valid = super(SignUpView, self).form_valid(form)
        user = form.save()

        scheme = self.request.scheme
        domain = get_current_site(self.request).domain

        test = get_user_model().objects.get(pk=user.id)
        print('SYSHESTVYE', test)

        send_verification_email.delay(user.id, scheme, domain)
        return valid


def activate_request(request):
    return render(request, 'users/activate_request.html')


class ActivateView(View):
    def get(self, request, uidb64, token):
        User = get_user_model()

        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(
                request,
                'Your account has been activated! You are now able to log in!'
            )
            return redirect('login')
        else:
            return HttpResponse('Invalid Token')
