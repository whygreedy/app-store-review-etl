import re

from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

from app_store_review_etl.pipeline.steps.step import Step


class UpdateGraph(Step):
    def process(self, gspread_client, inputs):
        credentials = Credentials.from_authorized_user_file('../authorized_user.json')
        drive_service = build('drive', 'v3', credentials=credentials)
        file_metadata = {'name': 'wordcloud.png'}
        media = MediaFileUpload('./wordcloud.png', mimetype='image/png')
        try:
            uploaded_image = drive_service.files().create(body=file_metadata, media_body=media, fields='id').execute()
            permission = {
                'type': 'anyone',
                'role': 'reader',
            }
            drive_service.permissions().create(fileId=uploaded_image['id'], body=permission).execute()
            image_url = f'https://drive.google.com/uc?export=view&id={uploaded_image["id"]}'
            print("Uploaded image URL:", image_url)
            self.update_top_likes_dislikes_analysis(gspread_client, inputs, image_url)
        except Exception as e:
            print(f'{type(e).__name__}: {e}')

    def update_top_likes_dislikes_analysis(self, gspread_client, inputs, image_url):
        spreadsheet_id = inputs['spreadsheet_id']

        spreadsheet = gspread_client.open_by_key(spreadsheet_id)
        worksheet3 = spreadsheet.worksheet('Sheet3')
        worksheet3.clear()
        res = worksheet3.append_row(['word cloud', '=IMAGE(\"{}\")'.format(image_url)],
                                    value_input_option='USER_ENTERED')

        width = 400
        height = 200
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
