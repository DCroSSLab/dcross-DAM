# DJANGO_SECRET_KEY = 'Enter your django secret key'
#
# # default amqp config
# CELERY_BROKER_URL = 'amqp://guest@localhost:5672/'
#
# CELERY_RESULT_BACKEND = 'mongodb://username:password@localhost:27017/?authSource=admin&authMechanism=SCRAM-SHA-256'
#
# CELERY_MONGODB_BACKEND_SETTINGS = {
#     'database': 'celery_results',
#     'taskmeta_collection': 'celery_taskmeta',
#     'user': 'username',
#     'password': 'password'
# }
#
# TWITTER_CONSUMER_API_KEY = ""
# TWITTER_CONSUMER_API_SECRET = ""
# TWITTER_ACCESS_TOKEN = ""
# TWITTER_ACCESS_TOKEN_SECRET = ""
# TWITTER_BOT_USERNAME = ""


DJANGO_SECRET_KEY = 'pdn3h8ww&q6lib5e!z#nm@-g943z-xz!h^jmdy-uqxc!pvm-o7'

CELERY_BROKER_URL = 'amqp://guest@localhost:5672/'
CELERY_RESULT_BACKEND = 'mongodb://faraaz:winterfell@localhost:27017/?authSource=admin&authMechanism=SCRAM-SHA-256'
# see firefox bookmark under eyic/celery and fix the result backend
CELERY_MONGODB_BACKEND_SETTINGS = {
    'database': 'celery_results2',
    'taskmeta_collection': 'celery_taskmeta2',
    'user': 'faraaz',
    'password': 'winterfell'}
TWITTER_CONSUMER_API_KEY = "6PafgtTnEyNQfc1VxkPSRkiC4"
TWITTER_CONSUMER_API_SECRET = "MX78oz3PfEBoZBR0T858aDs3plUhNB3YWPjhwvud8eePW83NiZ"
TWITTER_ACCESS_TOKEN = "1341030899249377281-GSFQ48FbXbJy5XQjCyc6cfeHIkM1Wx"
TWITTER_ACCESS_TOKEN_SECRET = "Ln5EVG0Jmu14FvKCUBQQekeFMMd73rhV4ZFSoR7X8xVK2"
TWITTER_BOT_USERNAME = "@dcross_bot"