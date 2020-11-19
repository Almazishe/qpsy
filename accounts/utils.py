from django.contrib.auth import get_user_model
User = get_user_model()

from bot.models import TelegramUser

from .models import SPECIALIST
from .models import ONLINE

def normalize_email(email):
    try:
        email_name, domain_part = email.strip().rsplit('@', 1)
    except ValueError as e:
        raise ValueError(e.args)
    else:
        email = email_name + '@' + domain_part.lower()
    return email


def get_the_most_free_spec():
    specialists = User.objects.filter(level=SPECIALIST, status=ONLINE)
    specialist = None
    min_count = TelegramUser.objects.all().count()

    for spec in specialists:
        if spec.get_clients_count() < min_count:
            specialist = spec
            min_count =  spec.get_clients_count()
    
    return specialist