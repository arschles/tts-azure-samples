import os
import requests
import time
from xml.etree import ElementTree

text = """
Despite long-standing availability of an effective vaccine, tetanus remains a significant problem in many countries. Outcome depends on access to mechanical ventilation and intensive care facilities and in settings where these are limited, mortality remains high. Administration of tetanus antitoxin by the intramuscular route is recommended treatment for tetanus, but as the tetanus toxin acts within the central nervous system, it has been suggested that intrathecal administration of antitoxin may be beneficial. Previous studies have indicated benefit, but with the exception of one small trial no blinded studies have been performed.
The objective of this study is to establish whether the addition of intrathecal tetanus antitoxin reduces the need for mechanical ventilation in patients with tetanus. Secondary objectives: to determine whether the addition of intrathecal tetanus antitoxin reduces autonomic nervous system dysfunction and length of hospital/ intensive care unit stay; whether the addition of intrathecal tetanus antitoxin in the treatment of tetanus is safe and cost-effective; to provide data to inform recommendation of human rather than equine antitoxin.
This study will enroll adult patients (>=16 years old) with tetanus admitted to the Hospital for Tropical Diseases, Ho Chi Minh City. The study is a 2x2 factorial blinded randomized controlled trial. Eligible patients will be randomized in a 1:1:1:1 manner to the four treatment arms (intrathecal treatment and human intramuscular treatment, intrathecal treatment and equine intramuscular treatment, sham procedure and human intramuscular treatment, sham procedure and equine intramuscular treatment).
"""


class TextToSpeech(object):
    def __init__(self, subscription_key):
        self.subscription_key = subscription_key
        self.tts = text
        self.timestr = time.strftime("%Y%m%d-%H%M")
        self.access_token = None

    def get_token(self):
        fetch_token_url = "https://eastus.api.cognitive.microsoft.com/sts/v1.0/issueToken"
        headers = {
            'Ocp-Apim-Subscription-Key': self.subscription_key
        }
        response = requests.post(fetch_token_url, headers=headers)
        self.access_token = str(response.text)
        print("got access token")

    def save_audio(self):
        base_url = 'https://eastus.tts.speech.microsoft.com/'
        path = 'cognitiveservices/v1'
        constructed_url = base_url + path
        headers = {
            'Authorization': 'Bearer ' + self.access_token,
            'Content-Type': 'application/ssml+xml',
            'X-Microsoft-OutputFormat': 'riff-24khz-16bit-mono-pcm',
            'User-Agent': 'YOUR_RESOURCE_NAME'
        }
        xml_body = ElementTree.Element('speak', version='1.0')
        xml_body.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-us')
        voice = ElementTree.SubElement(xml_body, 'voice')
        voice.set('{http://www.w3.org/XML/1998/namespace}lang', 'en-US')
        #####
        # Here's where you can set the different voices!
        # Check out https://docs.microsoft.com/en-us/azure/cognitive-services/speech-service/language-support#text-to-speech
        # for the full list, and copy the string under "Service name mapping"
        # to the second argument in the below 'voice.set' function
        #####
        voice.set(
            'name', 'Microsoft Server Speech Text to Speech Voice (en-US, ZiraRUS)'
        )
        prosody = ElementTree.SubElement(
            voice, "prosody", attrib={"rate": "-15.00%"})
        prosody.text = self.tts
        body = ElementTree.tostring(xml_body)

        response = requests.post(constructed_url, headers=headers, data=body)
        if response.status_code == 200:
            with open('sample-' + self.timestr + '.wav', 'wb') as audio:
                audio.write(response.content)
                print("\nStatus code: " + str(response.status_code) +
                      "\nYour TTS is ready for playback.\n")
        else:
            print("\nStatus code: " + str(response.status_code) +
                  "\nSomething went wrong. Check your subscription key and headers.\n")


if __name__ == "__main__":
    print("What's the subscription key?")
    subscription_key = raw_input()
    app = TextToSpeech(subscription_key)
    app.get_token()
    app.save_audio()
