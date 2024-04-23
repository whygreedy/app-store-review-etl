import gspread
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

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

        header = ['Polarity Score', 'Sentiment', 'Sentiment Emoji']
        data = [header]

        analyzer = SentimentIntensityAnalyzer()
        for review in worksheet.get('C2:C'):
            score_dict = analyzer.polarity_scores(review[0])
            compound_score = score_dict['compound']
            sentiment = self.classify_sentiment(compound_score)
            sentiment_emoji = self.classify_sentiment_emoji(compound_score)
            data.append([str(compound_score), str(sentiment), str(sentiment_emoji)])

        worksheet.update('E:G', data)

    def classify_sentiment(self, compound_score):
        if compound_score >= 0.05:
            return 'Positive'
        elif compound_score <= -0.05:
            return 'Negative'
        else:
            return 'Neutral'

    def classify_sentiment_emoji(self, compound_score):
        if compound_score >= 0.05:
            return '\U0001f600'
        elif compound_score <= -0.05:
            return '\U0001F621'
        else:
            return '\U0001F610'
