from conf.settings import *  # noqa

DATABASES = {"default": env.db("TEST_DATABASE_URL")}
UNIT_TESTING = True
CELERY_TASK_ALWAYS_EAGER = True
