from app_store_review_etl.pipeline.steps.step import Step


class Postflight(Step):
    def process(self, gspread_client, spreadsheet, inputs):
        spreadsheet_name = inputs['spreadsheet_name']
        sheet1 = spreadsheet.worksheet('Sheet1')
        spreadsheet.del_worksheet_by_id(sheet1.id)
        print(f'{spreadsheet_name} is ready: ', spreadsheet.url)
        print('POSTFLIGHT...')
