import gspread
import google.generativeai as genai

from app_store_review_etl.pipeline.steps.step import Step
from app_store_review_etl.settings import CREDENTIALS_GSPREAD_FILE_PATH
from app_store_review_etl.settings import GEMINI_API_KEY


class TopLikesDislikesAnalysis(Step):
    def process(self, token, inputs):
        reviews = self.read_reviews(inputs)
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.0-pro-latest')
        prompt = 'Given the following app reviews list, please generate ' \
                 'two numbered lists of the top ten things people ' \
                 'like or dislike about the app, listed from the most ' \
                 'prominent to the least prominent:\n' + str(reviews)

        print(model.count_tokens(prompt))
        print('prompt:', prompt)
        try:
            response = model.generate_content(
                contents=[prompt]
            )
            output_text = response.text
            print(output_text)
            output_data = []
            output_text_list = output_text.strip().split('\n')
            for output_text in output_text_list:
                output_data.append([output_text])
        except Exception as e:
            print(f'{type(e).__name__}: {e}')

        self.update_top_likes_dislikes_analysis(inputs, output_data)

    def read_reviews(self, inputs):
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

        reviews = []

        for review in worksheet.get('C2:C192'):
            reviews.append(review[0])
        return reviews

    def update_top_likes_dislikes_analysis(self, inputs, output_data):
        scopes = inputs['scopes']
        spreadsheet_id = inputs['spreadsheet_id']

        gc = gspread.oauth(
            credentials_filename=CREDENTIALS_GSPREAD_FILE_PATH,
            authorized_user_filename='../authorized_user.json',
            scopes=scopes,
        )

        spreadsheet = gc.open_by_key(spreadsheet_id)
        worksheet2 = spreadsheet.worksheet('Sheet2')
        worksheet2.clear()
        worksheet2.update('A1', output_data)
