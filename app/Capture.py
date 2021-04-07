import streamlink
import cv2
from datetime import datetime
import time
import os
import subprocess

twitch_prefix = 'twitch.tv/'
fps = 30.0
time_per_frame = 1.0 / fps

capture_seconds = int(os.getenv('CAPTURE_SECONDS', 60))
delay_seconds = int(os.getenv('DELAY_SECONDS', 18))


class Capture:

    _cap = None
    _file_name = None

    def record(self, twitch_user):
        successful = self._start_stream_capture(twitch_user)
        if not successful:
            return False

        self._initialise_file_name()

        self._delay()
        successful = self._record_to_file()

        if successful:
            self._compress()

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
        self._file_name = "キッカーカメラ_" + now.strftime("%H%M%S") + '.mp4'
        print("INFO: File name is: " + self._file_name)

    def _delay(self):
        # Delay recording purposely to handle the twitch stream lag
        print("INFO: Purposely delaying " + str(delay_seconds) +
              " seconds to handle stream delay")
        time.sleep(delay_seconds)

    def _record_to_file(self):
        width = int(self._cap.get(3))
        height = int(self._cap.get(4))

        fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        out = cv2.VideoWriter(self._file_name, fmt, fps, (width, height))
        print("INFO: Recording " + str(capture_seconds) + " seconds. " +
              "This might take long.")

        start_time = time.time()
        while time.time() - start_time < capture_seconds:

            time_before = time.time()

            successful, frame = self._cap.read()
            if successful:
                out.write(frame)

                # delay to match fps
                time_now = time.time()
                sleep_time = max(time_per_frame - (time_now - time_before), 0)
                time.sleep(sleep_time)
            else:
                out.release()
                print("ERROR: Failed to read frame from stream capture")
                return False

        out.release()

        print("INFO: Successfully finished recording")
        return True

    def _close_stream_capture(self):
        self._cap.release()

    def _compress(self):
        print("INFO: Compressing video, this may take long.")

        compressed_file_name = 'compressed_' + self._file_name
        subprocess.run(('ffmpeg -i ' + self._file_name + ' -vcodec libx265 -crf 28 -preset ultrafast' + compressed_file_name).split(),
                       stdout=subprocess.DEVNULL,
                       stderr=subprocess.STDOUT)
        subprocess.run(['mv', compressed_file_name, self._file_name])
        print("INFO: Finished compressing video")


if __name__ == "__main__":
    capture = Capture()
    successful = capture.record('insomniac')
    if successful:
        print("Recorded file: " + capture.get_file_name())
    else:
        print("Failed to record stream to file")
