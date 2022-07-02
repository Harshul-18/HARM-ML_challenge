from youtubeStatstics import YTStats

# Youtube v3 API from https://console.cloud.google.com/apis
API_KEY = "AIzaSyB7VRys9vS2-3tMmMWrSGkzaZheGu_ZW4w"

# Getting the channel id from https://commentpicker.com/youtube-channel-id.php 
# Currently using the Carryminati's youtube channel id
# channelId = "UCclJ1kaHxEC5P-VDZ_BsuJA"
channelId = "UCj22tfcQrWG7EMEKS0qLeEg"

# Creating a YTStats object named youtube
youtube = YTStats(API_KEY, channelId)
# Executing the getChannelStats method of YTStats object
youtube.getChannelStats()
# Executing the getChannelVideoData method of YTStats object
youtube.getChannelVideoData()
# Dumping or Writing the youtube object json text data in a file named channel name with extension of json file
youtube.dumpJSON()
