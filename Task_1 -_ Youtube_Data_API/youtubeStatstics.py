import requests
import json
# tqdm is used for progress bar in the terminal
from tqdm import tqdm

# TextColor class for printing different texts with specific color
class TextColor:
    # Heading
    HEADER = '\033[95m'
    # Just blue
    OKBLUE = '\033[94m'
    # Correct 
    OKCYAN = '\033[96m'
    # Success Green
    OKGREEN = '\033[92m'
    # Warning Yellow
    WARNING = '\033[93m'
    # Failure Red
    FAIL = '\033[91m'
    # Ending the color
    ENDC = '\033[0m'
    # Font weight = Bold
    BOLD = '\033[1m'
    # Underlining a text
    UNDERLINE = '\033[4m'

class YTStats:
    
    # YTStats Class Constructor
    def __init__(self, apiKey, channelId):
        # Setting the passed arguments to this class instances
        self.apiKey = apiKey
        self.channelId = channelId
        self.channelStats = None
        self.videoData = None

    # Getting the channel statistics
    def getChannelStats(self):
        # Forming the URL with the channel id and api key
        url = f'https://www.googleapis.com/youtube/v3/channels?part=statistics&id={self.channelId}&key={self.apiKey}'
        # Converting the URL data to json text
        jsonURL = requests.get(url)
        jsonText = jsonURL.text
        # Storing the json text to data
        data = json.loads(jsonText)
        # Extracting the channel statistics from the items key from the json text data with try except block
        try:
            data = data["items"][0]["statistics"]
        except:
            data = None
        # Returning the data and storing the data in the channel statistics
        self.channelStats = data
        return data

    # Method for getting the channel's video data
    def getChannelVideoData(self):
        # Getting the video ids
        channelVideos = self._getChannelVideos(limit=50)
        # Getting the video statistics
        parts = ["snippet", "statistics", "contentDetails"]
        # Running the progress bar using tqdm while looping through the videoId in channel videos
        for videoId in tqdm(channelVideos):
            # Looping through the parts
            for part in parts:
                # Getting the current video details using getSingleVideoData method
                data = self._getSingleVideoData(videoId, part)
                # Updating the channelVideos videoId dict with data
                channelVideos[videoId].update(data)
        # Storing the channel videos in this object's videoData variable
        self.videoData = channelVideos
        # Returning the channelVideos dict
        return channelVideos

    # Method for getting a specified video stats
    def _getSingleVideoData(self, videoId, part):
        # URL to get the single video json data stats
        url = f"https://www.googleapis.com/youtube/v3/videos?part={part}&id={videoId}&key={self.apiKey}"
        # Converting the URL to json URL
        jsonUrl = requests.get(url)
        # Loading the json URL in a python dictionary named data
        data = json.loads(jsonUrl.text)
        # Storing the video data if found, otherwise printing the error and storing an empty dictionary
        try:
            data = data["items"][0][part]
        except:
            print(TextColor.FAIL + f"{part.capitalize()} couldn't be found in items" + TextColor.ENDC)
            data = dict()
        # Returning the video data dictionary
        return data


    # Getting the channel videos
    def _getChannelVideos(self, limit=None):
        # URL to get all the channel videos with details
        url = f'https://www.googleapis.com/youtube/v3/search?key={self.apiKey}&channelId={self.channelId}&part=id&order=date'
        # Extending the URL, limiting the results, the url loads
        if limit is not None and isinstance(limit, int):
            url += "&maxResults=" + str(limit)
        # Getting the 
        vid, npt = self._getChannelVideosPerPage(url)
        idx = 0
        while (npt is not None and idx < 10):
            nextUrl = url + "&pageToken=" + npt
            nextVid, npt = self._getChannelVideosPerPage(nextUrl)
            vid.update(nextVid)
            idx += 1
        return vid
        
    # Getting the channel videos details per page with the URL
    def _getChannelVideosPerPage(self, url):
        # Converting and Loading the JSON URL to python data dictionary
        jsonUrl = requests.get(url)
        jsonText = jsonUrl.text
        data = json.loads(jsonText)
        # Creating an empty channelVideos dictionary
        channelVideos = dict()
        # Getting the json data items field to get the videos
        if 'items' not in data:
            return channelVideos, None
        itemData = data['items']
        nextPageToken = data.get("nextPageToken", None)
        # Looping through the item data
        for item in itemData:
            try:
                kind = item["id"]["kind"]
                if kind == "youtube#video":
                    videoId = item["id"]["videoId"]
                    channelVideos[videoId] = dict()
            except KeyError:
                print(TextColor.FAIL + "Item ID not found" + TextColor.ENDC)
        # Returning the channelVideos dict and nextPageToken
        return channelVideos, nextPageToken

    # Method for getting the channel title
    def getChannelTitle(self):
        # Extracting the channel title
        channelTitle = self.videoData.popitem()[1].get("channelTitle", self.channelId)
        return channelTitle

    # Method for dumping or writing the json text data to a file
    def dumpJSON(self):
        # Checking if the channel statistics is empty or not
        if not(self.channelStats is None or self.videoData is None):
            fusedData = {self.channelId: {"channelStatistics": self.channelStats, "videoData": self.videoData}}
            # Getting the channel title
            channelTitle = self.getChannelTitle()
            # Formatting the channel title
            channelTitle = channelTitle.replace(" ", "_").lower()
            # Creating the file name with extension ".json"
            fileName = channelTitle + ".json"
            # Openning the file in write mode
            with open(fileName, "w") as file:
                # Dumping or writing the channel statistics in the file with indent spaces count of 4
                json.dump(fusedData, file, indent=4)
        else:
            # Printing the error if data is none
            print(TextColor.FAIL + "Data is None" + TextColor.ENDC)
            return

    