import os
import re

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from app_store_review_etl.pipeline.steps.step import Step
from app_store_review_etl.logger import logger


class UpdateGraph(Step):
    def process(self, gspread_client, spreadsheet, inputs):
        logger.info('UPDATING GRAPHS INTO GOOGLE SHEET...')

        credentials = Credentials.from_authorized_user_file('../authorized_user.json')
        drive_service = build('drive', 'v3', credentials=credentials)

        title_worksheet = 'data_graphs'
        spreadsheet.add_worksheet(title=title_worksheet, rows=1000, cols=10)
        worksheet3 = spreadsheet.worksheet(title_worksheet)

        for file_name in os.listdir('./outputs'):
            file_metadata = {'name': file_name}
            media = MediaFileUpload(f'./outputs/{file_name}', mimetype='image/png')
            try:
                uploaded_image = drive_service.files().create(body=file_metadata, media_body=media,
                                                              fields='id').execute()
                permission = {
                    'type': 'anyone',
                    'role': 'reader'
                }
                drive_service.permissions().create(fileId=uploaded_image['id'], body=permission).execute()
                image_url = f'https://drive.google.com/uc?export=view&id={uploaded_image["id"]}'
                logger.info(f'uploaded image URL: {image_url}')

                res = worksheet3.append_row([file_name, '=IMAGE(\"{}\")'.format(image_url)],
                                            value_input_option='USER_ENTERED')
                width = 480
                height = 360
                row = int(re.findall("\\w+![A-Z]+([0-9]+)", res['updates']['updatedRange'], re.S)[0])
                requests = [{
                    "updateDimensionProperties": {
                        "properties": {
                            "pixelSize": height
                        },
                        "range": {
                            "sheetId": worksheet3.id,
                            "dimension": "ROWS",
                            "startIndex": row - 1,
                            "endIndex": row
                        },
                        "fields": "pixelSize"
                    }
                },
                    {
                        "updateDimensionProperties": {
                            "properties": {
                                "pixelSize": width
                            },
                            "range": {
                                "sheetId": worksheet3.id,
                                "dimension": "COLUMNS",
                                "startIndex": 1,
                                "endIndex": 2
                            },
                            "fields": "pixelSize"
                        }
                    }
                ]
                spreadsheet.batch_update({"requests": requests})

            except Exception as e:
                logger.debug(f'{type(e).__name__}: {e}')

        logger.info('COMPLETED UPDATING GRAPHS INTO GOOGLE SHEET.')
