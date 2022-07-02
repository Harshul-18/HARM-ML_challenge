import pandas as pd
import json
from youtubeCategoryIDList import categoryDict

name = "carryminati"
fileName = name + ".json"
data = None
with open(fileName, 'r') as file:
    data = json.load(file)

channelId, stats = data.popitem()
channelStats = stats["channelStatistics"]
videoStats = stats["videoData"]

print("views : ", channelStats["viewCount"])
print("subscriber : ", channelStats["subscriberCount"])
print("videos : ", channelStats["videoCount"])

sortedVids = sorted(
    videoStats.items(),
    key=lambda item: int(item[1]["viewCount"]),
    reverse=True,
)

stats = []
for vid in sortedVids:
    videoId = vid[0]
    title = vid[1]["title"]
    try:
        views = int(vid[1]["viewCount"])
        category = categoryDict[int(vid[1]["categoryId"])]
        likes = int(vid[1]["likeCount"])
        comments = int(vid[1]["commentCount"])
    except:
        views, category, likes, comments = 0, 0, 0, 0
    stats.append([title, views, category, likes, comments])

record = pd.DataFrame(
    stats,
    columns=[
        "title",
        "views",
        "category",
        "likes",
        "comments",
    ],
)

# First run in terminal:- "pip install openpyxl"
record.to_excel(name + ".xlsx")
print("DataFrame saved to excel file")
