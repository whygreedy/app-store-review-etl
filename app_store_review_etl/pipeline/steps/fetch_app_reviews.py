import datetime
from app_store_scraper import AppStore

from app_store_review_etl.pipeline.steps.step import Step
from app_store_review_etl.logger import logger


class FetchAppReviews(Step):
    def process(self, gspread_client, spreadsheet, inputs):
        logger.info('FETCHING APP REVIEWS...')

        app_country = inputs['app_country']
        app_name = inputs['app_name']
        date_after = inputs['date_after']

        date_part = date_after.split('-')
        year = int(date_part[0])
        month = int(date_part[1])
        day = int(date_part[2])
        datatime = datetime.datetime(year, month, day)

        try:
            target_app = AppStore(country=app_country, app_name=app_name)
            target_app.review(after=datatime)

            header = ['Date', 'Rating', 'Review', 'UserName']
            data = [header]
            reviews = []

            for review in target_app.reviews:
                reviews.append(review)

            for review in reviews:
                data.append([str(review['date']), str(review['rating']), review['review'], review['userName']])

            title_worksheet = 'reviews'
            spreadsheet.add_worksheet(title=title_worksheet, rows=1000, cols=10)
            worksheet = spreadsheet.worksheet(title_worksheet)
            worksheet.update('A1', data)

        except Exception as e:
            logger.info(f'{type(e).__name__}: {e}')

        logger.info('COMPLETED FETCHING APP REVIEWS.')
