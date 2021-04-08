import requests
import os
import threading

YOUR_API_KEY = 'a7a4ce2007b42d838d0e91b28c2a53d964d2706d'


class Upload:

    def upload(self, name):
        r = requests.get('https://send-anywhere.com/web/v1/device',
                         params={'profile_name': 'kicker_camera',
                                 'api_key': YOUR_API_KEY})

        device_key = r.json().get('device_key')
        cookies = {'device_key': device_key}

        size = os.path.getsize(name)
        print("INFO: video file size is: " + str(size))

        params = {'file': [{'name': name, 'size': size}]}
        r = requests.post('https://send-anywhere.com/web/v1/key',
                          json=params,
                          cookies=cookies).json()

        upload_link = r.get('weblink')
        key = r.get('key')
        print('INFO: Upload link is: ' + upload_link)
        print('INFO: SendAnywhere key is: ' + key)

        threading.Thread(
            target=self._p2p_transfer, args=(name, upload_link)).start()

        r = requests.get('https://send-anywhere.com/web/v1/key/' + key,
                         cookies=cookies).json()

        download_link = r.get('weblink')
        print('INFO: Download link is: ' + download_link)

        return download_link

    def _p2p_transfer(self, name, weblink):
        print("INFO: Started P2P transfer. Waiting for receiver.")
        video_file = open(name, 'rb')
        x = requests.post(weblink, files={'file': video_file})

        if x.status_code == 200:
            print("INFO: P2P transfer complete! Video successfully transferred.")
        else:
            print("ERROR: P2P transfer failed. This may be due to the 10 minute limit for SendAnywhere.")

        if os.path.exists(name):
            os.remove(name)


if __name__ == "__main__":
    Upload().upload('output.mp4')
