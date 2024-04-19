import os
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS_GSPREAD_FILE_PATH = os.getenv('CREDENTIALS_GSPREAD_FILE_PATH')
