import streamlink
import cv2
from datetime import datetime

num_frames = 150
twitch_prefix = 'twitch.tv/'


class Capture:

    _cap = None
    _file_name = None

    def record(self, twitch_user):
        successful = self._start_stream_capture(twitch_user)
        if not successful:
            return False

        self._initialise_file_name()

        successful = self._record_to_file()

        self._close_stream_capture()
        return successful

    def get_file_name(self):
        return self._file_name

    def _start_stream_capture(self, twitch_user):
        stream_name = twitch_prefix + twitch_user

        print("INFO: Attempting to connect to: " + stream_name)

        try:
            streams = streamlink.streams(stream_name)
        except streamlink.PluginError:
            print("ERROR: Streamlink PluginError. Please check that " +
                  twitch_user + " is an existing twitch username")
            return False
        except streamlink.NoPluginError:
            print("ERROR: Streamlink NoPluginError. No plugin for the URL " +
                  "was found.")
            return False

        if not streams:
            print("ERROR: Stream not active. Please check that the stream " +
                  "is up.")
            return False

        print("INFO: Available stream resolutions are: " + ", ".join(streams))

        url = streams['best'].url
        print("INFO: Selected streams resolution 'best'")

        print("INFO: Starting Video Capture")
        self._cap = cv2.VideoCapture(url)

        return True

    def _initialise_file_name(self):
        now = datetime.now()
        self._file_name = "動画" + now.strftime("%H時%M分%S秒") + '.mp4'
        print("INFO: File name is: " + self._file_name)

    def _record_to_file(self):
        width = int(self._cap.get(3))
        height = int(self._cap.get(4))

        fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        out = cv2.VideoWriter(self._file_name, fmt, 20.0, (width, height))

        print("INFO: Recording " + str(num_frames) + " frames. " +
              "This might take long.")
        for _ in range(num_frames):
            successful, frame = self._cap.read()
            if successful:
                out.write(frame)
            else:
                out.release()
                print("ERROR: Failed to read frame from stream capture")
                return False

        out.release()

        print("INFO: Successfully finished recording")
        return True

    def _close_stream_capture(self):
        self._cap.release()


if __name__ == "__main__":
    capture = Capture()
    successful = capture.record('insomniac')
    if successful:
        print("Recorded file: " + capture.get_file_name())
    else:
        print("Failed to record stream to file")