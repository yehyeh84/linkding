import logging
from django.conf import settings
from django.contrib.auth import user_logged_in, user_login_failed
from django.db.backends.signals import connection_created
from django.dispatch import receiver

from bookmarks.services import tasks

logger = logging.getLogger(__name__)

##FROM https://stackoverflow.com/questions/37618473/how-can-i-log-both-successful-and-failed-login-and-logout-attempts-in-django
def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


@receiver(user_logged_in)
def user_logged_in(sender, request, user, **kwargs):
    tasks.schedule_bookmarks_without_snapshots(user)
    ip = get_client_ip(request)
    logger.info(f'Login success. username={user},  ip={ip}')

@receiver(user_login_failed)
def user_login_failed_recv(sender, credentials, request, **kwargs):
    username=credentials.get('username')
    ip = get_client_ip(request)
    logger.warn(f'Login failed. username={username},  ip={ip}')


@receiver(connection_created)
def extend_sqlite(connection=None, **kwargs):
    # Load ICU extension into Sqlite connection to support case-insensitive
    # comparisons with unicode characters
    if connection.vendor == 'sqlite' and settings.USE_SQLITE_ICU_EXTENSION:
        connection.connection.enable_load_extension(True)
        connection.connection.load_extension(settings.SQLITE_ICU_EXTENSION_PATH.rstrip('.so'))

        with connection.cursor() as cursor:
            # Load an ICU collation for case-insensitive ordering.
            # The first param can be a specific locale, it seems that not
            # providing one will use a default collation from the ICU project
            # that works reasonably for multiple languages
            cursor.execute("SELECT icu_load_collation('', 'ICU');")
