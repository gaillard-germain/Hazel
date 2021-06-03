import os
from dotenv import load_dotenv
from .base import *


load_dotenv()

ENVIRONMENT = os.getenv("ENVIRONMENT", os.getenv("ENV"))

if ENVIRONMENT == "staging":
   from .staging import *
elif ENVIRONMENT == "production":
   from .production import *
else:
   from .local import *
