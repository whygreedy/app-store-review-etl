import os.path

from app_store_scraper import AppStore
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError


# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = ''
SAMPLE_RANGE_NAME = 'Sheet1!A1'
clearedRange = 'Sheet1'


def get_api_data():
    flushtoiletfinder = AppStore(country="us", app_name="flush-toilet-finder-map")
    flushtoiletfinder.review()

    header = ['Date', 'Rating', 'Review', 'UserName']
    data = [header]
    reviews = []

    for review in flushtoiletfinder.reviews:
        reviews.append(review)

    for review in reviews:
        data.append([str(review['date']), str(review['rating']), review['review'], review['userName']])

    return data


def main():
    """Shows basic usage of the Sheets API.
    Prints values from a sample spreadsheet.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('../credentials.json', SCOPES)
            creds = flow.run_local_server(port=3000)
            # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Data to be loaded
        # valueData = [["Bing", "Cindy", "Cloudy", "Grace", "Jeans", "Billy"]]
        # valueData = read_file()
        value_data = get_api_data()

        # Call the Sheets API
        sheet = service.spreadsheets()
        # Clear all the values in the sheet first
        result = sheet.values().clear(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=clearedRange).execute()
        # Update the sheet with the data
        result = sheet.values().update(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME,
                                       valueInputOption="USER_ENTERED", body={'values': value_data}).execute()

    except HttpError as err:
        print(err)


if __name__ == "__main__":
    main()
