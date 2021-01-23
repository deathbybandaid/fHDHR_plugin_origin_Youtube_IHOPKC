import datetime

PLUGIN_NAME = "youtube"
PLUGIN_VERSION = "v0.6.0-beta"
PLUGIN_TYPE = "alt_epg"


class YOUTUBE_Setup():
    def __init__(self, config):
        pass


class youtubeEPG():

    def __init__(self, fhdhr, channels):
        self.fhdhr = fhdhr

        self.channels = channels

    def get_channel_thumbnail(self, videoid):
        if "channel_thumbnail" not in list(self.channels.origin.video_reference[videoid].keys()):

            channel_id = self.channels.origin.video_reference[videoid]["channel_id"]
            channel_api_url = ('https://www.googleapis.com/youtube/v3/channels?id=%s&part=snippet,contentDetails&key=%s' %
                               (channel_id, str(self.fhdhr.config.dict["youtube"]["api_key"])))
            channel_response = self.fhdhr.web.session.get(channel_api_url)
            channel_data = channel_response.json()

            self.channels.origin.video_reference[videoid]["channel_thumbnail"] = channel_data["items"][0]["snippet"]["thumbnails"]["high"]["url"]

        return self.channels.origin.video_reference[videoid]["channel_thumbnail"]

    def get_content_thumbnail(self, content_id):
        return ("https://i.ytimg.com/vi/%s/maxresdefault.jpg" % (str(content_id)))

    def update_epg(self):
        programguide = {}

        timestamps = []
        xtimestart = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        xtimeend = xtimestart + datetime.timedelta(days=6)
        xtime = datetime.datetime.today().replace(hour=0, minute=0, second=0, microsecond=0)
        while xtime <= xtimeend:
            timestampdict = {
                            "time_start": xtime.timestamp(),
                            "time_end": (xtime + datetime.timedelta(hours=1)).timestamp(),
                            }
            xtime = xtime + datetime.timedelta(hours=1)
            timestamps.append(timestampdict)

        for c in self.channels.get_channels():

            if str(c["number"]) not in list(programguide.keys()):
                programguide[str(c["number"])] = {
                                                    "callsign": c["callsign"] or c["name"],
                                                    "name": c["name"],
                                                    "number": c["number"],
                                                    "id": c["origin_id"],
                                                    "thumbnail": self.get_channel_thumbnail(c["origin_id"]),
                                                    "listing": [],
                                                    }

            for timestamp in timestamps:
                clean_prog_dict = {
                                    "time_start": timestamp['time_start'],
                                    "time_end": timestamp['time_end'],
                                    "duration_minutes": 60,
                                    "thumbnail": self.get_content_thumbnail(c["origin_id"]),
                                    "title": self.channels.origin.video_reference[c["origin_id"]]["title"],
                                    "sub-title": "Unavailable",
                                    "description": self.channels.origin.video_reference[c["origin_id"]]["description"],
                                    "rating": "N/A",
                                    "episodetitle": None,
                                    "releaseyear": None,
                                    "genres": [],
                                    "seasonnumber": None,
                                    "episodenumber": None,
                                    "isnew": False,
                                    "id": "%s_%s" % (c["origin_id"], str(timestamp['time_start']).split(" ")[0]),
                                    }

                programguide[str(c["number"])]["listing"].append(clean_prog_dict)

        return programguide
