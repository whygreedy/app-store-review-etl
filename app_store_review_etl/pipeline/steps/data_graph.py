from wordcloud import WordCloud
from wordcloud import STOPWORDS

from app_store_review_etl.pipeline.steps.step import Step


class DataGraph(Step):
    def process(self, gspread_client, inputs):
        reviews = self.read_reviews(gspread_client, inputs)

        stopwords = set(STOPWORDS)
        stopwords.update(['app'])
        wc = WordCloud(background_color="white", max_words=2000,
                       contour_width=3, contour_color='steelblue',
                       stopwords=stopwords)

        wordcloud = wc.generate(reviews)
        image = wordcloud.to_image()
        print(type(image))
        image.show()
        image.save('wordcloud.png')

    def read_reviews(self, gspread_client, inputs):
        spreadsheet_id = inputs['spreadsheet_id']
        range_worksheet = inputs['range_worksheet']

        spreadsheet = gspread_client.open_by_key(spreadsheet_id)
        worksheet = spreadsheet.worksheet(range_worksheet)

        reviews = ''

        for review in worksheet.get('C2:C'):
            reviews += str(review[0])
        return reviews
