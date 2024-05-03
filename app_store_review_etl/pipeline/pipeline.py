from app_store_review_etl.pipeline.steps.step import StepException


class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def run(self, gspread_client, inputs):
        for step in self.steps:
            try:
                step().process(gspread_client, inputs)
            except StepException as e:
                print(e)
                break
