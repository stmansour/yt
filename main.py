from ytstats import YTstats

yt = YTstats()
data = yt.get_channel_stats()
yt.save_to_file()
