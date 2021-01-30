import pafy


class Plugin_OBJ():

    def __init__(self, plugin_utils):
        self.plugin_utils = plugin_utils

        self.video_reference = {}
        self.channel_id = "UCqSYig9Cmx6DJ3XaUYg4vpw"

    def get_channels(self):

        channel_api_url = ('https://www.googleapis.com/youtube/v3/search?channelId=%s&order=date&eventType=live&type=video&key=%s&part=snippet'
                           % (self.channel_id, str(self.plugin_utils.config.dict["youtube"]["api_key"])))
        channel_api_response = self.plugin_utils.web.session.get(channel_api_url)
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
                                            "video_id": video_id,
                                            "thumbnail": "https://yt3.ggpht.com/a/AATXAJyF27VVvcRYjnggXVY8NVwND68nWqzpXj5zaB2tUg=s176-c-k-c0x00ffffff-no-rj-mo"
                                            }

        return [clean_station_item]

    def get_channel_stream(self, chandict, stream_args):
        pafyobj = pafy.new(self.video_reference[chandict["origin_id"]]["video_id"])
        streamurl = str(pafyobj.getbest().url)

        stream_info = {"url": streamurl}

        return stream_info