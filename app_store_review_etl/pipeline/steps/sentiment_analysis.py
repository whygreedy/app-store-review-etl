import gspread
from textblob import TextBlob

from app_store_review_etl.pipeline.steps.step import Step
from app_store_review_etl.settings import CREDENTIALS_GSPREAD_FILE_PATH


class SentimentAnalysis(Step):
    def process(self, token, inputs):
        scopes = inputs['scopes']
        spreadsheet_id = inputs['spreadsheet_id']
        range_worksheet = inputs['range_worksheet']

        gc = gspread.oauth(
            credentials_filename=CREDENTIALS_GSPREAD_FILE_PATH,
            authorized_user_filename='../authorized_user.json',
            scopes=scopes,
        )

        spreadsheet = gc.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(range_worksheet)

        header = ['Polarity', 'Subjectivity']
        data = [header]

        for review in worksheet.get('C2:C'):
            review_sentiment = TextBlob(review[0])
            polarity = review_sentiment.sentiment.polarity
            subjectivity = review_sentiment.sentiment.subjectivity
            data.append([str(polarity), str(subjectivity)])

        worksheet.update('E:F', data)
