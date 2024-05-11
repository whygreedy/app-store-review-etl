import gspread

from app_store_review_etl.settings import CREDENTIALS_GSPREAD_FILE_PATH


class GoogleSheetsAuth:
    @staticmethod
    def google_sheets_auth():
        scopes = ['https://www.googleapis.com/auth/drive.file']

        gc = gspread.oauth(
            credentials_filename=CREDENTIALS_GSPREAD_FILE_PATH,
            authorized_user_filename='../authorized_user.json',
            scopes=scopes,
        )

        return gc
