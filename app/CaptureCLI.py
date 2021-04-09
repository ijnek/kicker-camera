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


class CaptureCLI:

    _cap = None
    _file_name = None

    def record(self, twitch_user):

        self._initialise_file_name()

        self._delay()

        bashCmd = ["streamlink", "twitch.tv/insomniac", "best", "-o", self._file_name]
        process = subprocess.Popen(bashCmd, stdout=subprocess.PIPE)

        time.sleep(capture_seconds)
        process.kill()

        return True

    def get_file_name(self):
        return self._file_name

    def _initialise_file_name(self):
        now = datetime.utcnow()
        self._file_name = "キッカーカメラ_" + now.strftime("%H%M%S%f") + '.mp4'
        print("INFO: File name is: " + self._file_name)

    def _delay(self):
        # Delay recording purposely to handle the twitch stream lag
        print("INFO: Purposely delaying " + str(delay_seconds) +
              " seconds to handle stream delay")
        time.sleep(delay_seconds)


if __name__ == "__main__":
    capture = CaptureCLI()
    successful = capture.record('insomniac')
    if successful:
        print("Recorded file: " + capture.get_file_name())
    else:
        print("Failed to record stream to file")
