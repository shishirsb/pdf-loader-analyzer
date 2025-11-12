import os

class API:
    def __init__(self):
        self.OPENAI_API_KEY = "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"

    def set_api_key(self):
        os.environ["OPENAI_API_KEY"] = self.OPENAI_API_KEY

    


    