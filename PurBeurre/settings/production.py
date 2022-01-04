from . import *
import sentry_sdk
from sentry_sdk.integrations.django import DjangoIntegration
import raven
import dj_database_url

DEBUG = False
ALLOWED_HOSTS= ['165.232.112.10']


MIDDLEWARE.insert(
    MIDDLEWARE.index('django.middleware.security.SecurityMiddleware')+1,
    'whitenoise.middleware.WhiteNoiseMiddleware'
    )


db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)


INSTALLED_APPS_EXTENDED = [
    'raven.contrib.django.raven_compat',
]
INSTALLED_APPS.extend(INSTALLED_APPS_EXTENDED)


LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'INFO',  # WARNING by default.
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s '
                      '%(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            # To capture more than ERROR, change to WARNING, INFO, etc.
            'level': 'INFO',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
            'tags': {'custom-tag': 'x'},
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

sentry_sdk.init(
    dsn="https://d42e418337c0497ca27ee7012c862b71@o1055791" +
        ".ingest.sentry.io/6041945",
    integrations=[DjangoIntegration()],

    # Set traces_sample_rate to 1.0 to capture 100%
    # of transactions for performance monitoring.
    # We recommend adjusting this value in production.
    traces_sample_rate=1.0,

    # If you wish to associate users to errors (assuming you are using
    # django.contrib.auth) you may enable sending PII data.
    send_default_pii=True
)

RAVEN_CONFIG = {
    'dsn': 'https://somethingverylong@sentry.io/6041945',
    # If you are using git, you can also automatically configure the
    # release based on the git info.
    'release': raven.fetch_git_sha(os.path.dirname(os.pardir)),
}
