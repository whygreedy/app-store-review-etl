from app_store_review_etl.pipeline.steps.step import StepException


class Pipeline:
    def __init__(self, steps):
        self.steps = steps

    def run(self, gspread_client, spreadsheet, inputs):
        for step in self.steps:
            step_instance = step()
            try:
                step_instance.process(gspread_client, spreadsheet, inputs)
            except StepException as e:
                print(e)
                break
