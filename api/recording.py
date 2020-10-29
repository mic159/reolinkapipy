import requests
import random
import string
from urllib import parse
from io import BytesIO
from PIL import Image
from RtspClient import RtspClient


class RecordingAPIMixin:
    """API calls for recording/streaming image or video."""
    def get_recording_encoding(self) -> object:
        """
        Get the current camera encoding settings for "Clear" and "Fluent" profiles.
        See examples/response/GetEnc.json for example response data.
        :return: response json
        """
        body = [{"cmd": "GetEnc", "action": 1, "param": {"channel": 0}}]
        return self._execute_command('GetEnc', body)

    def get_recording_advanced(self) -> object:
        """
        Get recording advanced setup data
        See examples/response/GetRec.json for example response data.
        :return: response json
        """
        body = [{"cmd": "GetRec", "action": 1, "param": {"channel": 0}}]
        return self._execute_command('GetRec', body)

    ###########
    # RTSP Stream
    ###########
    def open_video_stream(self, profile: str = "main") -> Image:
        """
        profile is "main" or "sub"
        https://support.reolink.com/hc/en-us/articles/360007010473-How-to-Live-View-Reolink-Cameras-via-VLC-Media-Player
        :param profile:
        :return:
        """
        with RtspClient(ip=self.ip, username=self.username, password=self.password,
                        proxies={"host": "127.0.0.1", "port": 8000}) as rtsp_client:
            rtsp_client.preview()

    def get_snap(self, timeout: int = 3) -> Image or None:
        """
        Gets a "snap" of the current camera video data and returns a Pillow Image or None
        :param timeout: Request timeout to camera in seconds
        :return: Image or None
        """
        data = {}
        data['cmd'] = 'Snap'
        data['channel'] = 0
        data['rs'] = ''.join(random.choices(string.ascii_uppercase + string.digits, k=10))
        data['user'] = self.username
        data['password'] = self.password
        parms = parse.urlencode(data).encode("utf-8")

        try:
            response = requests.get(self.url, params=parms, timeout=timeout)
            if response.status_code == 200:
                return Image.open(BytesIO(response.content))
            print("Could not retrieve data from camera successfully. Status:", response.stats_code)
            return None

        except Exception as e:
            print("Could not get Image data\n", e)
            raise
