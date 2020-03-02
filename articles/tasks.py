from celery import task
from django.contrib.auth import get_user_model
from articles.models import Comment


@task
def send_notification_email(author_id, comment_id):
    User = get_user_model()

    try:
        user = User.objects.get(pk=author_id)
        comment = Comment.objects.get(pk=comment_id)
        text = f'Someone commented your article "{comment.article.title}"'

        user.email_user("New comment", text, 'admin@admin.com')
    except (User.DoesNotExist, Comment.DoesNotExist) as e:
        print(e)