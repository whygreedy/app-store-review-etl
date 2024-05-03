import google.generativeai as genai

from app_store_review_etl.pipeline.steps.step import Step
from app_store_review_etl.settings import GEMINI_API_KEY


class TopLikesDislikesAnalysis(Step):
    def process(self, gspread_client, inputs):
        reviews = self.read_reviews(gspread_client, inputs)
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.0-pro-latest')

        final_reviews = []
        sum_tokens = 0
        count_reviews = 0
        for review in reviews:
            review_tokens = model.count_tokens(review).total_tokens
            sum_tokens += (review_tokens + 2)
            if sum_tokens < 28000:
                count_reviews += 1
                print('sum_tokens: ', sum_tokens, 'count_reviews: ', count_reviews)
                final_reviews.append(review)
            else:
                break

        prompt = 'Given the following app reviews list, please generate ' \
                 'two numbered lists of the top ten things people ' \
                 'like or dislike about the app, listed from the most ' \
                 'prominent to the least prominent:\n' + str(final_reviews)

        print('prompt:', prompt)
        print(model.count_tokens(prompt))

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

        self.update_top_likes_dislikes_analysis(gspread_client, inputs, output_data)

    def read_reviews(self, gspread_client, inputs):
        spreadsheet_id = inputs['spreadsheet_id']
        range_worksheet = inputs['range_worksheet']

        spreadsheet = gspread_client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(range_worksheet)

        reviews = []

        for review in worksheet.get('C2:C'):
            reviews.append(review[0])
        return reviews

    def update_top_likes_dislikes_analysis(self, gspread_client, inputs, output_data):
        spreadsheet_id = inputs['spreadsheet_id']

        spreadsheet = gspread_client.open_by_key(spreadsheet_id)
        worksheet2 = spreadsheet.worksheet('Sheet2')
        worksheet2.clear()
        worksheet2.update('A1', output_data)
