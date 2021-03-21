import streamlink
import cv2
from datetime import datetime

num_frames = 150

class Capture:

    def record(self):
        streams = streamlink.streams('twitch.tv/kenjibrameld')

        if not streams:
            print("Stream not found/active")
            return None

        url = streams['best'].url
        cap = cv2.VideoCapture(url)

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        name = "recording_" + current_time + '.mp4'

        width = int(cap.get(3))
        height = int(cap.get(4))

        fmt = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        out = cv2.VideoWriter(name, fmt, 20.0, (width, height))

        for _ in range(num_frames):
            succ, frame = cap.read()
            if succ:
                # cv2.imshow("Capturing",frame)
                out.write(frame)

            else:
                break

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        out.release()

        return name