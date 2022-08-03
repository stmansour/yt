import json

class YTstats:
    def __init__(self):
        #------------------------------------
        # Get the config information
        #------------------------------------
        f = open('config.json')
        data = json.load(f)
        print(data)
        f.close()
        self.api_key = data["API_KEY"]
        self.channel_id = data["CHANNEL_ID"]

    def get_channel_stats(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.api_key}&key={self.channel_id}'
        print(url)
