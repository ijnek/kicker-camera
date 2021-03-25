import requests
import urllib.request
import os
import threading

YOUR_API_KEY = 'a7a4ce2007b42d838d0e91b28c2a53d964d2706d'


class Upload:

    def upload(self, name):
        r = requests.get('https://send-anywhere.com/web/v1/device',
                         params={'profile_name': 'testlinebotpython',
                                 'api_key': YOUR_API_KEY})

        device_key = r.json().get('device_key')
        cookies = {'device_key': device_key}

        size = os.path.getsize(name)
        print("INFO: video file size is: " + str(size))

        params = {'file': [{'name': name, 'size': size}]}
        r = requests.post('https://send-anywhere.com/web/v1/key',
                          json=params,
                          cookies=cookies).json()

        weblink = r.get('weblink')
        key = r.get('key')
        print('INFO: Upload link is: ' + weblink)
        print('INFO: SendAnywhere key is: ' + key)

        threading.Thread(
            target=self._p2p_transfer, args=(name, weblink)).start()

        print("here")

        r = requests.get('https://send-anywhere.com/web/v1/key/' + key,
                         cookies=cookies).json()

        return r.get('weblink')

    def _p2p_transfer(self, name, weblink):
        print("INFO: Started P2P transfer. Waiting for receiver.")
        video_file = open(name, 'rb')
        x = requests.post(weblink, files={'file': video_file})
        print(x.json())
        print("INFO: P2P transfer complete! Video successfully transfered.")

    # # Working download function
    # def download(self, key):

    #     r = requests.get('https://send-anywhere.com/web/v1/device',
    #                      params={'profile_name': 'testlinebotpython', 'api_key': YOUR_API_KEY})

    #     device_key = r.json().get('device_key')
    #     cookies = {'device_key': device_key}

    #     r = requests.get('https://send-anywhere.com/web/v1/key/' + key, cookies=cookies)
    #     print(r.url)
    #     print(r.text)

    #     download_url = r.json().get('weblink')
    #     print("download_url: " + str(download_url))

    #     download_file_name = key + '_downloaded.mp4'  # WE DONT KNOW THE EXTENSION OF THE FILE!!
    #     response = urllib.request.urlretrieve(download_url, download_file_name)
    #     print(response[1].get_content_type())

    #     print("Saved to " + download_file_name)


if __name__ == "__main__":
    Upload().upload('output.mp4')
