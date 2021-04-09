import cv2
from datetime import datetime
import time
import os
import subprocess

twitch_prefix = 'twitch.tv/'

capture_seconds = int(os.getenv('CAPTURE_SECONDS', 60))
delay_seconds = int(os.getenv('DELAY_SECONDS', 18))


class TwitchCapture:

    _cap = None
    _file_name = None

    def record(self, twitch_user):

        self._initialise_file_name()

        self._delay()
        successful = self._record_to_file(twitch_user)

        return successful

    def _record_to_file(self, twitch_user):
        stream_name = twitch_prefix + twitch_user
        
        print("INFO: Attempting to record " + str(capture_seconds) + " seconds from " + stream_name +
              ". This might take long.")

        bashCmd = ["streamlink", stream_name, "best", "-o", self._file_name]
        process = subprocess.Popen(bashCmd, stdout=subprocess.DEVNULL,
                                   stderr=subprocess.DEVNULL)
        try:
            process.communicate(timeout=capture_seconds)[0]
        except subprocess.TimeoutExpired:
            process.terminate()
            print("INFO: Successfully finished recording")
            return True

        print("ERROR: Can't find stream. Please check that the stream " +
              "name is correct and is active")
        return False

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
    capture = TwitchCapture()
    successful = capture.record('kenjibrameld')
    if successful:
        print("Recorded file: " + capture.get_file_name())
    else:
        print("Failed to record stream to file")
