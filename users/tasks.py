from django.urls import reverse
from .tokens import account_activation_token
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth import get_user_model
from celery import task
from celery import shared_task


@shared_task
def send_verification_email(user_id, scheme, domain):
    User = get_user_model()

    try:
        print('before')
        print(user_id)
        user = User.objects.get(pk=user_id)

        print('after')

        kwargs = {
            'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': account_activation_token.make_token(user)
        }

        url = reverse('activate', kwargs=kwargs)
        activation_link = f'{scheme}://{domain}{url}'
        subject = 'Activate account'
        text = f'Activate account: {activation_link}'

        user.email_user(subject, text)
    except User.DoesNotExist as e:
        print(e)
