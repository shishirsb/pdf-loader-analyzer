import os

class API:
    def __init__(self):
        self.OPENAI_API_KEY = "<api-key>"
    def set_api_key(self):
        os.environ["OPENAI_API_KEY"] = self.OPENAI_API_KEY

    


    