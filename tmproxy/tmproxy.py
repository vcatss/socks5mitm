import requests

class TMPRoxy:
    def __init__(self,url,api_key, timeout=30):
        self.url = "https://tmproxy.com/api/proxy"
        self.api_key = api_key

    def check(self):
        #post data to https://tmproxy.com/api/proxy/stats and get response
        data = {"api_key": f"{self.api_key}"}
        response = requests.post(self.url + "/stats", data=data)
        print(self.url + "/stats")
        print(data)
        print(response.text)

    def getCurrentProxy(self):
        #post data to https://tmproxy.com/api/proxy and get response
        data = {"api_key": self.api_key}
        response = requests.post(self.url + '/get-current-proxy', data=data, timeout=30)
        print(response.text)

        