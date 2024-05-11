import os

from wordcloud import WordCloud
from wordcloud import STOPWORDS

from app_store_review_etl.pipeline.steps.step import Step
from app_store_review_etl.settings import OUTPUTS_DIR


class WordCloudGraph(Step):
    def process(self, gspread_client, spreadsheet, inputs):

        worksheet = spreadsheet.worksheet('reviews')
        reviews = ''
        for review in worksheet.get('C2:C'):
            reviews += str(review[0])

        try:
            stopwords = set(STOPWORDS)
            stopwords.update(['app'])
            wc = WordCloud(
                background_color="white", max_words=2000, contour_width=3,
                contour_color='steelblue', stopwords=stopwords
            )

            wordcloud = wc.generate(reviews)
            image = wordcloud.to_image()
            output_filepath = os.path.join(OUTPUTS_DIR, 'wordcloud.png')
            image.save(output_filepath)

        except Exception as e:
            print(f'{type(e).__name__}: {e}')
