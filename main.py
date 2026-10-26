import os
from dotenv import load_dotenv
from utils.hallo import sag_hallo

load_dotenv()

print(os.getenv("SECRET_KEY"))
print(sag_hallo("Chef"))