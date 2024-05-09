import os

from app_store_review_etl.settings import OUTPUTS_DIR

class Utils:
    def __init__(self):
        pass

    def create_dirs(self):
        os.makedirs(OUTPUTS_DIR, exist_ok=True)
