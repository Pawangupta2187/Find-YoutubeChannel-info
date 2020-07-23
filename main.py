from youtube_stats import YTstats

channel_statistics =None
video_data=None
API_KEY="AIzaSyCwQ3WJ4ieNE3M_YXi3N0ShL59oyN0i0xo"
channel_id = "UCj22tfcQrWG7EMEKS0qLeEg"
yt = YTstats(API_KEY,channel_id)

channel_statistics=yt.get_channel_statitics()
video_data=yt.get_channel_video_data()
#channel_stats=yt.dump()
print(channel_statistics)
print(video_data.popitem()[1].get('channelTitle', channel_id))