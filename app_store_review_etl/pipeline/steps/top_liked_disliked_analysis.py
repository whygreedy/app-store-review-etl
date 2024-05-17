import google.generativeai as genai
from nltk.tokenize.casual import TweetTokenizer

from app_store_review_etl.pipeline.steps.step import Step
from app_store_review_etl.settings import GEMINI_API_KEY
from app_store_review_etl.logger import logger


class TopLikedDislikedAnalysis(Step):
    def process(self, gspread_client, spreadsheet, inputs):
        logger.info('ANALYZING TOP LIKES/DISLIKES FEATURES BY GEMINI MODEL...')

        # google gemini ai model config
        genai.configure(api_key=GEMINI_API_KEY)
        ai_model = inputs['ai_model']
        model = genai.GenerativeModel(ai_model)

        # read reviews from Sheet1 and generate prompt
        try:
            worksheet = spreadsheet.worksheet('reviews')
            final_reviews = []
            sum_tokens = 0
            count_reviews = 0
            for review in worksheet.get('C2:C'):
                review_tokens = self.count_token(review[0])
                sum_tokens += (review_tokens + 2)
                if sum_tokens < 28000:
                    count_reviews += 1
                    logger.info(f'sum_tokens: {sum_tokens}, count_reviews: {count_reviews}')
                    final_reviews.append(review[0])
                else:
                    break

            prompt = 'Given the following app reviews list, please generate ' \
                     'top ten things people like and top ten things people dislike ' \
                     'about the app into two numbered lists in English, listed from the most ' \
                     'prominent to the least prominent:\n' + str(final_reviews)

            logger.info(f'prompt: {prompt}')
            logger.info(f'{model.count_tokens(prompt)}')

            # get response and update response to google sheet
            response = model.generate_content(
                contents=[prompt]
            )
            output_text = response.text
            logger.info(f'{output_text}')
            output_data = []
            output_text_list = output_text.strip().split('\n')
            for output_text in output_text_list:
                output_data.append([output_text])

            title_worksheet = 'top_analysis'
            spreadsheet.add_worksheet(title=title_worksheet, rows=1000, cols=10)
            worksheet2 = spreadsheet.worksheet(title_worksheet)
            worksheet2.update('A1', output_data)

        except Exception as e:
            logger.info(f'{type(e).__name__}: {e}')

        logger.info('COMPLETED ANALYZING TOP LIKES/DISLIKES FEATURES.')

    def count_token(self, review):
        tokenizer = TweetTokenizer()
        token_list = tokenizer.tokenize(review)
        token_count = len(token_list)
        return token_count
