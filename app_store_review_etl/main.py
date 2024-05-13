from app_store_review_etl.google_sheets_auth.google_sheets_auth import GoogleSheetsAuth
from app_store_review_etl.pipeline.pipeline import Pipeline
from app_store_review_etl.pipeline.steps.preflight import Preflight
from app_store_review_etl.pipeline.steps.fetch_app_reviews import FetchAppReviews
from app_store_review_etl.pipeline.steps.sentiment_analysis import SentimentAnalysis
from app_store_review_etl.pipeline.steps.top_likes_dislikes_analysis import TopLikesDislikesAnalysis
from app_store_review_etl.pipeline.steps.word_cloud_graph import WordCloudGraph
from app_store_review_etl.pipeline.steps.graph import Graph
from app_store_review_etl.pipeline.steps.update_graph import UpdateGraph
from app_store_review_etl.pipeline.steps.postflight import Postflight


SPREADSHEET_NAME = 'final-cut-pro_app_review_analysis'
APP_COUNTRY = 'us'
APP_NAME = 'figma'


def main():

    inputs = {
        'spreadsheet_name': SPREADSHEET_NAME,
        'app_country': APP_COUNTRY,
        'app_name': APP_NAME,
    }

    steps = [
                Preflight,
                FetchAppReviews,
                SentimentAnalysis,
                TopLikesDislikesAnalysis,
                WordCloudGraph,
                Graph,
                UpdateGraph,
                Postflight,
            ]

    gspread_client = GoogleSheetsAuth.google_sheets_auth()
    spreadsheet_name = inputs['spreadsheet_name']
    spreadsheet = gspread_client.create(spreadsheet_name)
    p = Pipeline(steps)
    p.run(gspread_client, spreadsheet, inputs)


if __name__ == "__main__":
    main()
