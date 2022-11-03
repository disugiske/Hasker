import os

from dotenv import load_dotenv
load_dotenv()

print(list(os.getenv("ALLOWED_HOSTS")))