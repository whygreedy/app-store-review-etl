import google.generativeai as genai

from app_store_review_etl.pipeline.steps.step import Step
from app_store_review_etl.settings import GEMINI_API_KEY


class TopLikesDislikesAnalysis(Step):
    def process(self, gspread_client, spreadsheet, inputs):

        # google gemini ai model config
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel('gemini-1.0-pro-latest')

        # read reviews from Sheet1 and generate prompt
        try:
            worksheet = spreadsheet.worksheet('reviews')
            final_reviews = []
            sum_tokens = 0
            count_reviews = 0
            for review in worksheet.get('C2:C'):
                review_tokens = model.count_tokens(review[0]).total_tokens
                sum_tokens += (review_tokens + 2)
                if sum_tokens < 28000:
                    count_reviews += 1
                    print('sum_tokens: ', sum_tokens, 'count_reviews: ', count_reviews)
                    final_reviews.append(review[0])
                else:
                    break

            prompt = 'Given the following app reviews list, please generate ' \
                     'two numbered lists of the top ten things people ' \
                     'like or dislike about the app, listed from the most ' \
                     'prominent to the least prominent:\n' + str(final_reviews)

            print('prompt:', prompt)
            print(model.count_tokens(prompt))

        except Exception as e:
            print(f'{type(e).__name__}: {e}')

        # get response and update response to google sheet
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

            title_worksheet = 'top_analysis'
            spreadsheet.add_worksheet(title=title_worksheet, rows=1000, cols=10)
            worksheet2 = spreadsheet.worksheet(title_worksheet)
            worksheet2.update('A1', output_data)

        except Exception as e:
            print(f'{type(e).__name__}: {e}')
