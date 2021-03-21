import streamlink
import cv2
from datetime import datetime

num_frames = 150

def record():
    streams = streamlink.streams('twitch.tv/kenjibrameld')

    if not streams:
        print("Stream not found/active")
        return None

    url = streams['best'].url
    cap = cv2.VideoCapture(url)

    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    name = "recording_" + current_time + '.avi'

    width = int(cap.get(3))
    height = int(cap.get(4))

    fourcc = cv2.VideoWriter_fourcc(*'MPEG')
    out = cv2.VideoWriter(name, fourcc, 20.0, (width,height))

    # while True:

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
