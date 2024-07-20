####################################################################################################
# API Keys and other Auths
# This file centralizes the api key location for easy updating
####################################################################################################
import os

# Both cat and dog API keys can be obtained from: https://portal.thatapicompany.com/ for free. Add them here, within the quotes
CAT_API_KEY = ""  # cat as a service api key
DOG_API_KEY = "" # dog as a service api key

# usually you'd want to store keys and auth info in a .env file... lets add that functionality just because we can
CAT_API_KEY = os.environ.get('CAT_API_KEY') if os.environ.get('CAT_API_KEY') else CAT_API_KEY
DOG_API_KEY = os.environ.get('DOG_API_KEY') if os.environ.get('DOG_API_KEY') else DOG_API_KEY