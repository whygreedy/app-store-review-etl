import os

import matplotlib.pyplot as plt

from app_store_review_etl.pipeline.steps.step import Step
from app_store_review_etl.settings import OUTPUTS_DIR
from app_store_review_etl.logger import logger


class Graph(Step):
    def process(self, gspread_client, spreadsheet, inputs):
        logger.info('PLOTTING DISTRIBUTION GRAPHS...')

        # read data from Sheet1 and store data in a dictionary
        worksheet = spreadsheet.worksheet('reviews')
        try:
            ratings = []
            for rating in worksheet.get('B2:B'):
                ratings.append(str(rating[0]))

            polarity_scores = []
            for polarity in worksheet.get('E2:E'):
                polarity_scores.append(str(polarity[0]))

            sentiments = []
            for sentiment in worksheet.get('F2:F'):
                sentiments.append(str(sentiment[0]))

            data = {
                'ratings': ratings,
                'polarity_scores': polarity_scores,
                'sentiments': sentiments
            }

            # plot distribution of sentiment
            sentiments_data = {
                'Negative': data['sentiments'].count('Negative'),
                'Neutral': data['sentiments'].count('Neutral'),
                'Positive': data['sentiments'].count('Positive')
            }
            fig, ax = plt.subplots()
            sentiment_type = list(sentiments_data.keys())
            sentiment_count = list(sentiments_data.values())
            ax.bar(sentiment_type, sentiment_count, color=['tomato', 'gold', 'forestgreen'])
            ax.set_title('Distribution of sentiment')
            ax.set_xlabel('Sentiment')
            ax.set_ylabel('Count')
            output_filepath = os.path.join(OUTPUTS_DIR, 'sentiment.png')
            plt.savefig(output_filepath, dpi=500)

            # plot distribution of polarity score
            polarity_scores = [float(score) for score in data['polarity_scores']]
            fig, ax = plt.subplots()
            ax.hist(polarity_scores, bins=10, color='slategrey')
            ax.set_title('Distribution of polarity score')
            ax.set_xlabel('Polarity')
            ax.set_ylabel('Count')
            output_filepath = os.path.join(OUTPUTS_DIR, 'polarity.png')
            plt.savefig(output_filepath, dpi=500)

            # plot distribution of app rating
            rating_data = {
                '5': data['ratings'].count('5'),
                '4': data['ratings'].count('4'),
                '3': data['ratings'].count('3'),
                '2': data['ratings'].count('2'),
                '1': data['ratings'].count('1')
            }
            fig, ax = plt.subplots()
            rating = list(rating_data.keys())
            count = list(rating_data.values())
            ax.barh(rating, count, color='lightsteelblue')
            ax.set_title('Distribution of app rating')
            ax.set_xlabel('Count')
            ax.set_ylabel('Rating')
            output_filepath = os.path.join(OUTPUTS_DIR, 'rating.png')
            plt.savefig(output_filepath, dpi=500)

        except Exception as e:
            logger.debug(f'{type(e).__name__}: {e}')

        logger.info('COMPLETED PLOTTING DISTRIBUTION GRAPHS.')
