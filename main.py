from ytstats import YTstats

yt = YTstats()
stats = yt.get_channel_statistics()
vids = yt.get_channel_video_data()
yt.save_to_file()

for key,value in vids.items():
    print(value["viewCount"] + " " + value["title"])
