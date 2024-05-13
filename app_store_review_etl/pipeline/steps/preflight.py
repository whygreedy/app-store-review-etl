from app_store_review_etl.pipeline.steps.step import Step
from app_store_review_etl.utils import Utils
from app_store_review_etl.logger import logger


class Preflight(Step):
    def process(self, gspread_client, spreadsheet, inputs):
        logger.info('IN PREFLIGHT...')
        utils = Utils()
        utils.create_dirs()
