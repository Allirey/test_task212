from django.urls import reverse
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from celery import shared_task
from django.template.loader import render_to_string


@shared_task
def send_verification_email(user_id, scheme, domain, email_template=None):
    User = get_user_model()

    try:
        user = User.objects.get(pk=user_id)
        kwargs = {
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        }

        url = reverse('activate', kwargs=kwargs)
        activation_link = f'{scheme}://{domain}{url}'
        subject = 'Activate account'

        if email_template:
            text = render_to_string(email_template,
                                    {'scheme': scheme, 'domain': domain, 'activation_url': url, 'user': user})
        else:
            text = f'Activate account: {activation_link}'

        user.email_user(subject, text)
    except User.DoesNotExist as e:
        print(e)
