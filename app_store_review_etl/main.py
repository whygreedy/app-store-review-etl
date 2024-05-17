import sys
import getopt
sys.path.append('../')

from app_store_review_etl.google_sheets_auth.google_sheets_auth import GoogleSheetsAuth
from app_store_review_etl.pipeline.pipeline import Pipeline
from app_store_review_etl.pipeline.steps.preflight import Preflight
from app_store_review_etl.pipeline.steps.fetch_app_reviews import FetchAppReviews
from app_store_review_etl.pipeline.steps.sentiment_analysis import SentimentAnalysis
from app_store_review_etl.pipeline.steps.top_liked_disliked_analysis import TopLikedDislikedAnalysis
from app_store_review_etl.pipeline.steps.word_cloud_graph import WordCloudGraph
from app_store_review_etl.pipeline.steps.graph import Graph
from app_store_review_etl.pipeline.steps.update_graph import UpdateGraph
from app_store_review_etl.pipeline.steps.postflight import Postflight


APP_COUNTRY = 'us'
APP_NAME = 'youtube-watch-listen-stream'
DATE_AFTER = '2024-1-1'
AI_MODEL = 'gemini-1.0-pro-latest'


def print_usage():
    print('python3 main.py -c <app_country> -n <app_name> -d <date_after> -m <ai_model>')
    print('python3 main.py --app_country <app_country> --app_name <app_name> '
          '--date_after <date_after> --ai_model <ai_model>')

    print('python3 main.py OPTIONS')
    print('OPTIONS:')
    print('{:>10} {:<20}{}'.format('-c', '--app_country', 'The part of app store URL that indicates region or country'))
    print('{:>10} {:<20}{}'.format('-n', '--app_name', 'The part of app store URL that indicates the name of the app'))
    print('{:>10} {:<20}{}'.format('-d', '--date_after', 'Review recency. Default is fetching reviews after 2024-1-1'))
    print('{:>10} {:<20}{}'.format('-m', '--ai_model', 'Google AI model to be used. Default is gemini-1.0-pro-latest'))


def main():

    inputs = {
        'app_country': APP_COUNTRY,
        'app_name': APP_NAME,
        'date_after': DATE_AFTER,
        'ai_model': AI_MODEL,
    }

    short_opts = 'c:n:d:m:h'
    long_opts = 'help app_country= app_name= date_after= ai_model='.split()

    try:
        opts, args = getopt.getopt(sys.argv[1:], short_opts, long_opts)
    except getopt.GetoptError:
        print_usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print_usage()
            sys.exit(0)
        elif opt in ("-c", "--app_country"):
            inputs['app_country'] = arg
        elif opt in ("-n", "--app_name"):
            inputs['app_name'] = arg
        elif opt in ("-d", "--date_after"):
            inputs['date_after'] = arg
        elif opt in ("-m", "--ai_model"):
            inputs['ai_model'] = arg
        else:
            print_usage()
            sys.exit(2)

    steps = [
                Preflight,
                FetchAppReviews,
                SentimentAnalysis,
                TopLikedDislikedAnalysis,
                WordCloudGraph,
                Graph,
                UpdateGraph,
                Postflight,
            ]

    gspread_client = GoogleSheetsAuth.google_sheets_auth()
    spreadsheet_name = inputs['app_name'] + '_app_review_analysis'
    spreadsheet = gspread_client.create(spreadsheet_name)
    p = Pipeline(steps)
    p.run(gspread_client, spreadsheet, inputs)


if __name__ == "__main__":
    main()
