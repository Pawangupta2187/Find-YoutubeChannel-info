import json
import pandas as pd

file = "carryminati.json"
data =None
with open(file,'r') as f:
    data=json.load(f)

channel_id,stats=data.popitem()
channel_stats=stats['channel_statistics']
video_stats=stats['video_data']

print(channel_id)
#video statistic sort
sorted_vids= sorted(video_stats.items(),key=lambda item: int(item[1]["viewCount"]),reverse=True)
stats=[]
for video in sorted_vids:

    video_id=video[0]
    title =video[1]['title']
    views = int(video[1]['viewCount'])
    likes = int(video[1]['likeCount'])
    dislikes = int(video[1]['dislikeCount'])
    comments=int(video[1]['commentCount'])
    stats.append([video_id,title,views,likes,dislikes,comments])
df=pd.DataFrame(stats,columns=['video_id','title','views','likes','dislikes','comments'])
print(df.head(5))
top10videos=df.head(10)
for i in range(len(top10videos)):
    print(top10videos.iloc[i]['comments'])

#ax=top10videos.plot.bar(x="title",y="views",figsize=(12,8),fontsize=12)
import matplotlib.pyplot as plt
plt.bar(top10videos['title'],top10videos['views'])
plt.xlabel("Title")
plt.ylabel("Views")
plt.title("view based on title")
plt.show()
# f = plt.figure()
#plt.plot.bar(x="title",y="views",figsize=(12,8),fontsize=12)
# plt.show()
plt.savefig("bar-graph.pdf", bbox_inches='tight')
