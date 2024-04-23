from app_store_review_etl.pipeline.pipeline import Pipeline
from app_store_review_etl.pipeline.steps.preflight import Preflight
from app_store_review_etl.pipeline.steps.fetch_app_reviews import FetchAppReviews
from app_store_review_etl.pipeline.steps.sentiment_analysis import SentimentAnalysis

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
SPREADSHEET_ID = ''
RANGE_WORKSHEET = 'Sheet1'
APP_COUNTRY = 'us'
APP_NAME = 'canva-design-art-ai-editor'


def main():

    inputs = {
        'scopes': SCOPES,
        'spreadsheet_id': SPREADSHEET_ID,
        'range_worksheet': RANGE_WORKSHEET,
        'app_country': APP_COUNTRY,
        'app_name': APP_NAME,
    }

    steps = [
                Preflight,
                FetchAppReviews,
                SentimentAnalysis,
            ]

    p = Pipeline(steps)
    p.run(inputs)


if __name__ == "__main__":
    main()

