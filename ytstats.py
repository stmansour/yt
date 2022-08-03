import json
import requests

class YTstats:
    def __init__(self):
        #------------------------------------
        # Get the config information
        #------------------------------------
        f = open('config.json')
        data = json.load(f)
        f.close()
        self.api_key = data["API_KEY"]
        self.channel_id = data["CHANNEL_ID"]

    def get_channel_stats(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&key={self.api_key}&id={self.channel_id}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data["items"][0]["statistics"]
        except:
            data = None
        self.channel_stats = data
        return data

    def save_to_file(self):
        if self.channel_stats is None:
            return
        channel_title = "Steve Mansour Music"
        filestr = channel_title.replace(" ", "_").lower()
        filestr += ".json"
        with open(filestr,'w') as f:
            json.dump(self.channel_stats, f, indent=4)
        print("saved: " + filestr)
