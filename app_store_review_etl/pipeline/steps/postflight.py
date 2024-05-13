from app_store_review_etl.pipeline.steps.step import Step
from app_store_review_etl.logger import logger


class Postflight(Step):
    def process(self, gspread_client, spreadsheet, inputs):
        logger.info('IN POSTFLIGHT...')

        spreadsheet_name = inputs['spreadsheet_name']
        sheet1 = spreadsheet.worksheet('Sheet1')
        spreadsheet.del_worksheet_by_id(sheet1.id)
        logger.info(f'{spreadsheet_name} is ready: {spreadsheet.url}')
        logger.info('ALL COMPLETED!')
