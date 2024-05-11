from app_store_review_etl.pipeline.steps.step import Step
from app_store_review_etl.utils import Utils


class Preflight(Step):
    def process(self, gspread_client, spreadsheet, inputs):
        print('PREFLIGHT...')
        utils = Utils()
        utils.create_dirs()
