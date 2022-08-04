import json
import requests
from tqdm import tqdm

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
        self.channel_statistics = None
        self.video_data = None

    def get_channel_statistics(self):
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&key={self.api_key}&id={self.channel_id}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data["items"][0]["statistics"]
        except:
            data = None
        self.channel_statistics = data
        return data

    def save_to_file(self):
        if self.channel_statistics is None or self.video_data is None:
            print('data has not been loaded')
            return
        fused_data = {self.channel_id: {"channel_statistics": self.channel_statistics, "video_data": self.video_data}}
        channel_title = self.video_data.popitem()[1].get('channelTitle',self.channel_id)
        filestr = channel_title.replace(" ", "_").lower()
        filestr += ".json"
        with open(filestr,'w') as f:
            json.dump(fused_data , f, indent=4)
        print("saved: " + filestr)

    def get_channel_video_data(self):
        #-------------------------------
        # get all the video ids here
        #-------------------------------
        channel_videos = self._get_channel_videos(limit=16)
        print(len(channel_videos))
        #-------------------------------
        # get video statistics
        #-------------------------------
        parts = ["snippet", "statistics", "contentDetails"]
        for video_id in tqdm(channel_videos):
            for part in parts:
                data = self._get_video_part_data(video_id,part)
                channel_videos[video_id].update(data)
        self.video_data = channel_videos
        return channel_videos


    def _get_video_part_data(self, video_id, part):
        url = f'https://www.googleapis.com/youtube/v3/videos?part={part}&id={video_id}&key={self.api_key}'
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        try:
            data = data["items"][0][part]
        except:
            print("_get_video_part_data: error")
            data = dict()
        return data


    def _get_channel_videos(self, limit=None):
        url = f'https://www.googleapis.com/youtube/v3/search?key={self.api_key}&channelId={self.channel_id}&part=id&order=date'
        if limit is not None and isinstance(limit,int):
            url += "&maxResults=" + str(limit)
        vid, npt = self._get_channel_videos_part(url)
        print("NextPageToken = " + npt)
        idx = 0  # safeguard -- we'll limit to 10 tries if something goes wrong
        while (npt is not None and idx < 10):
            nexturl = url + "&pageToken=" + npt
            nextvid, npt = self._get_channel_videos_part(nexturl)
            vid.update(nextvid)
            idx += 1
        return vid


    def _get_channel_videos_part(self,url):
        json_url = requests.get(url)
        data = json.loads(json_url.text)
        channel_videos = dict()
        if 'items' not in data:
            return channel_videos, None
        nextPageToken = data.get("nextPageToken",None)
        item_data = data["items"]
        for item in item_data:
            try:
                kind = item['id']['kind']
                if kind == 'youtube#video':
                    video_id = item['id']['videoId']
                    channel_videos[video_id] = dict()
            except KeyError:
                print("KeyError")

        return channel_videos, nextPageToken
