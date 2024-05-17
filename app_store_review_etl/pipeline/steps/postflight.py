from app_store_review_etl.pipeline.steps.step import Step
from app_store_review_etl.logger import logger


class Postflight(Step):
    def process(self, gspread_client, spreadsheet, inputs):
        logger.info('IN POSTFLIGHT...')
        sheet1 = spreadsheet.worksheet('Sheet1')
        spreadsheet.del_worksheet_by_id(sheet1.id)
        logger.info('ALL COMPLETED!')
        logger.info(f'Output Google Sheet is ready: {spreadsheet.url}')
