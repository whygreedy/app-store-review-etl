from app_store_review_etl.pipeline.steps.step import Step


class Preflight(Step):
    def process(self, token, inputs):
        print('PREFLIGHT...')
