"""interface for the adafruit IO"""

import urequests
import ujson

class AdafruitIO:

    def __init__(self, username, key, base_url = 'https://io.adafruit.com/api/v2/'):
        """_summary_

        Args:
            username (str): username for login to adafruit io
            key (str): api string to loginto adafruit io
            base_url (str, optional): baseurl for adafruit_io.  Do not expect this to change but 
                optionally can be changed. Defaults to 'https://io.adafruit.com/api/v2/'.
        """
        self.username = username
        self.key = key
        self.base_url = base_url
    
    def send(self, value, url):
        """sends the data to adafruit IO.  feed_url is optional and will be derived from
        class if not provided.  

        Args:
            data (float or int): value to send to the api
            feed_url (_type_, optional): url to send data to.  This should not include username as this
                is input by the method based off class. Defaults to None.
        """
        # builds this out since we don't want the user to provide entire url...
        # maybe we shoudl... to be determined
        feed_url = self.base_url + str(self.username) + url
        headers = {'x-aio-key': self.key,
                'Content-Type': 'application/json',
                }
        data = {'value': value}
        response = urequests.post(url=feed_url, headers=headers, data=ujson.dumps(data))
        print('api post status code: {}'.format(response.status_code))