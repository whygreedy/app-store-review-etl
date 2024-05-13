from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

from app_store_review_etl.pipeline.steps.step import Step
from app_store_review_etl.logger import logger


class SentimentAnalysis(Step):
    def process(self, gspread_client, spreadsheet, inputs):
        logger.info('ANALYZING SENTIMENT...')

        worksheet = spreadsheet.worksheet('reviews')

        try:
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
            worksheet.freeze(rows=1)
            worksheet.sort((1, 'des'))

        except Exception as e:
            logger.debug(f'{type(e).__name__}: {e}')

        logger.info('COMPLETED ANALYZING SENTIMENT.')

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
