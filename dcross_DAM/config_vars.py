DJANGO_SECRET_KEY = 'Enter your django secret key'

# default amqp config
CELERY_BROKER_URL = 'amqp://guest@localhost:5672/'

CELERY_RESULT_BACKEND = 'mongodb://username:password@localhost:27017/?authSource=admin&authMechanism=SCRAM-SHA-256'

CELERY_MONGODB_BACKEND_SETTINGS = {
    'database': 'celery_results',
    'taskmeta_collection': 'celery_taskmeta',
    'user': 'username',
    'password': 'password'
}

TWITTER_CONSUMER_API_KEY = ""
TWITTER_CONSUMER_API_SECRET = ""
TWITTER_ACCESS_TOKEN = ""
TWITTER_ACCESS_TOKEN_SECRET = ""
TWITTER_BOT_USERNAME = ""