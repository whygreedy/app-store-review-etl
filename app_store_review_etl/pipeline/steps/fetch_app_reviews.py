import gspread
from app_store_scraper import AppStore

from app_store_review_etl.pipeline.steps.step import Step
from app_store_review_etl.settings import CREDENTIALS_GSPREAD_FILE_PATH


class FetchAppReviews(Step):
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
        worksheet.clear()

        value_data = self.fetch_app_reviews(inputs)
        worksheet.update('A1', value_data)

    def fetch_app_reviews(self, inputs):
        app_country = inputs['app_country']
        app_name = inputs['app_name']
        flush_toilet_finder = AppStore(country=app_country, app_name=app_name)
        flush_toilet_finder.review()

        header = ['Date', 'Rating', 'Review', 'UserName']
        data = [header]
        reviews = []

        for review in flush_toilet_finder.reviews:
            reviews.append(review)

        for review in reviews:
            data.append([str(review['date']), str(review['rating']), review['review'], review['userName']])

        return data
