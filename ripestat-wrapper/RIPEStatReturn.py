import json

class RIPEStatReturn():
    def __init__(self, response):
        self.response = response
        self.code = response.status_code
        self.reason = response.reason
        self.endpoint = response.url
        self.body = json.loads(response.text)

        self.query_time = self.body['time']
        self.data = self.body['data']

    def get_data_attributes(self):
        return list(self.data.keys())
    
    def get_data(self):
        return self.data

