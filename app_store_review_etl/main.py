from app_store_review_etl.google_sheets_auth.google_sheets_auth import GoogleSheetsAuth
from app_store_review_etl.pipeline.pipeline import Pipeline
from app_store_review_etl.pipeline.steps.preflight import Preflight
from app_store_review_etl.pipeline.steps.fetch_app_reviews import FetchAppReviews
from app_store_review_etl.pipeline.steps.sentiment_analysis import SentimentAnalysis
from app_store_review_etl.pipeline.steps.top_likes_dislikes_analysis import TopLikesDislikesAnalysis

SPREADSHEET_ID = ''
RANGE_WORKSHEET = 'Sheet1'
APP_COUNTRY = 'us'
APP_NAME = 'toilet-finder'


def main():

    inputs = {
        'spreadsheet_id': SPREADSHEET_ID,
        'range_worksheet': RANGE_WORKSHEET,
        'app_country': APP_COUNTRY,
        'app_name': APP_NAME,
    }

    steps = [
                Preflight,
                FetchAppReviews,
                SentimentAnalysis,
                TopLikesDislikesAnalysis,
            ]

    gspread_client = GoogleSheetsAuth.google_sheets_auth()
    p = Pipeline(steps)
    p.run(gspread_client, inputs)


if __name__ == "__main__":
    main()
