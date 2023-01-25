import requests

class MinProxy:
    def __init__(self,url,api_key, timeout=30):
        self.url = "https://dash.minproxy.vn/api/rotating/v1/proxy"
        self.api_key = api_key

    def getCurrentProxy(self):
        #import cookies as string
        cookies = " XSRF-TOKEN=eyJpdiI6IlkyS0J4ZGVYOEdqVXF2NmRMQVB1U3c9PSIsInZhbHVlIjoiaHFRb0crMW5tZzVXcHVDRnhOUHVvbWpNNDlWR2ZyZkp3ZGZZeSszdExDdDV6bEREeWNyazlENEtDUjJkYXY5Y1lSY0piQlBmR3ZmdGZPMVRjUVdWNFNQbEVhekJTOU0yNUpjWG9Hc3prSGxVYU8rSVwvaVV5SXpMejNUd2ZNME4zIiwibWFjIjoiMmQ2MzUxYjIyM2M1ZWI4YjRkOTcxMWRkNzJkNWMxZTMxY2Q5NGRmZjIzNzk0NjZmZGVhYThlMmZlNjIxMDI2MiJ9; laravel_session=eyJpdiI6IlRQUG5jWW5Td0pGM1p0bVBEWVZETUE9PSIsInZhbHVlIjoibUYrYkNzcDdxWEhkSUQ2MHRDMXV6eTdISGMxUkNubld1eEFWaFdaMWtBdk5XcVp3RytwU1dRZ1BqXC9XNjc4Q2twQnl1a1RFXC9cL1RwQTRsUU0wa0x4YmpJMG52bXBwbmE2M0NlMXFlOXppc05PMUpycUE0NStwVFpYc1BwZlcxMkoiLCJtYWMiOiI1NjlmYjUwMTllOWNlYmYyODUwOWQ3ZWViM2IwNTEwM2JmZGNjNWFmNjNmZGY1MDc4NTM3NzIyMzYwNzgxODNiIn0%3D"
        #convert cookies to dict
        cookies = dict(x.split("=") for x in cookies.split("; "))
        #get current proxy
        response = requests.get(self.url + "/get-current-proxy" + "?api_key=" + self.api_key, cookies=cookies, timeout=30)
        #html decode
        response = response.text.encode('utf-8').decode('unicode_escape')
        print(response)

    def getNewProxy(self):
        #import cookies as string
        cookies = " XSRF-TOKEN=eyJpdiI6IlkyS0J4ZGVYOEdqVXF2NmRMQVB1U3c9PSIsInZhbHVlIjoiaHFRb0crMW5tZzVXcHVDRnhOUHVvbWpNNDlWR2ZyZkp3ZGZZeSszdExDdDV6bEREeWNyazlENEtDUjJkYXY5Y1lSY0piQlBmR3ZmdGZPMVRjUVdWNFNQbEVhekJTOU0yNUpjWG9Hc3prSGxVYU8rSVwvaVV5SXpMejNUd2ZNME4zIiwibWFjIjoiMmQ2MzUxYjIyM2M1ZWI4YjRkOTcxMWRkNzJkNWMxZTMxY2Q5NGRmZjIzNzk0NjZmZGVhYThlMmZlNjIxMDI2MiJ9; laravel_session=eyJpdiI6IlRQUG5jWW5Td0pGM1p0bVBEWVZETUE9PSIsInZhbHVlIjoibUYrYkNzcDdxWEhkSUQ2MHRDMXV6eTdISGMxUkNubld1eEFWaFdaMWtBdk5XcVp3RytwU1dRZ1BqXC9XNjc4Q2twQnl1a1RFXC9cL1RwQTRsUU0wa0x4YmpJMG52bXBwbmE2M0NlMXFlOXppc05PMUpycUE0NStwVFpYc1BwZlcxMkoiLCJtYWMiOiI1NjlmYjUwMTllOWNlYmYyODUwOWQ3ZWViM2IwNTEwM2JmZGNjNWFmNjNmZGY1MDc4NTM3NzIyMzYwNzgxODNiIn0%3D"
        #convert cookies to dict
        cookies = dict(x.split("=") for x in cookies.split("; "))
        #get current proxy
        response = requests.get(self.url + "/get-new-proxy" + "?api_key=" + self.api_key, cookies=cookies, timeout=30)
        #html decode
        response = response.text.encode('utf-8').decode('unicode_escape')
        print(response)
        