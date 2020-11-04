import pafy


class OriginChannels():

    def __init__(self, settings, origin, logger, web):
        self.config = settings
        self.origin = origin
        self.logger = logger
        self.web = web

        self.video_reference = {}
        self.channel_id = "UCqSYig9Cmx6DJ3XaUYg4vpw"

    def get_channels(self):

        channel_api_url = ('https://www.googleapis.com/youtube/v3/search?channelId=%s&order=date&eventType=live&type=video&key=%s&part=snippet'
                           % (self.channel_id, str(self.config.dict["youtube"]["api_key"])))
        channel_api_response = self.web.session.get(channel_api_url)
        channel_api_data = channel_api_response.json()

        video_id = channel_api_data["items"][0]["id"]["videoId"]

        clean_station_item = {
                                "name": "IHOP Prayer Room",
                                "callsign": "International House of Prayer",
                                "id": self.channel_id,
                                }

        self.video_reference = {}
        self.video_reference[self.channel_id] = {
                                            "title": channel_api_data["items"][0]["snippet"]["title"],
                                            "description": channel_api_data["items"][0]["snippet"]["description"],
                                            "channel_id": self.channel_id,
                                            "channel_name": channel_api_data["items"][0]["snippet"]["channelTitle"],
                                            "video_id": video_id
                                            }

        return [clean_station_item]

    def get_channel_stream(self, chandict, allchandict):
        caching = False
        pafyobj = pafy.new(self.video_reference[chandict["id"]]["video_id"])
        streamlist = [
                        {
                         "number": chandict["number"],
                         "stream_url": str(pafyobj.getbest().url)
                         }
                    ]
        return streamlist, caching
