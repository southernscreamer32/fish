import openai
import sounddevice as sd
from TTS.api import TTS
import numpy as np
import pyrubberband as pyrb
import queue, threading, time
import requests
import torch

class TextToSpeech():
    # text to speech handlesdropping 
    # curr_playing = False
    audio = []
    def __init__(self):
        # x = torch.rand(5, 3)
        # print(x)
        # print(torch.cuda.is_available())

        self.name = 'Sakana'
        description = f'{self.name} is a fish being livestreamed on Twitch. She is quite arrogant about the size of her tank.'
        # print(description)
        requests.put('http://localhost:5000/api/v1/model', headers={'accept': 'application/json', 'Content-Type': 'application/json'}, data='{"model": "PygmalionAI/pygmalion-6b"}')
        requests.put('http://localhost:5000/api/v1/config/authors_note',
                     headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                     data=f'{{"value": "{description}"}}').json()
        requests.put('http://localhost:5000/api/v1/config/authors_note_template',
                     headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                     data='{"value": [Author\'s note: <|>]}"')
        requests.put('http://localhost:5000/api/v1/config/temperature', headers={'accept': 'application/json'}, data='{"value": 0.5}')
        requests.put('http://localhost:5000/api/v1/config/max_length', headers={'accept': 'application/json'}, data='{"value": 200}')
        requests.put('http://localhost:5000/api/v1/config/frmtrmblln',headers={'accept': 'application/json'},data='{"value": false}')

        self.tts = TTS("tts_models/en/vctk/vits", gpu=False)
        
        # audio stuff
        self.curr_playing = False
        self.delay = 1  #delay in secs before saying something new
        self.last_speak = time.time()

        # fish_thread = threading.Thread(target=self.try_fishspeak_loop, daemon=True)
        # fish_thread.start()
        # sd.default.device
        # print(self.audio_device.name)
        # self.audio_device = sd.query_devices("virtual audio cable") #change name to match actual device name!
        # if self.audio_device:
        #     self.audio_device = self.audio_device[0].name
        # else:
        #     self.audio_device = sd.default.device[1]
        # self.audio_stream = sd.OutputStream(samplerate=22050)

    def chat(self,prompt):
        prompt = f"You:{prompt}\\n{self.name}:"
        return requests.post('http://localhost:5000/api/v1/generate',
                             headers={'accept': 'application/json', 'Content-Type': 'application/json'},
                             data=f'{{"prompt": \"{prompt}\"}}').json()['results'][0]['text']
        # print(u)
    # def audio_callback(outdata, frames, time, status):
    #     print("AAA")
    #     if TextToSpeech.curr_playing:
    #
    #     # if self.curr_playing:
    #         outdata[:] = TextToSpeech.audio
    #         print(len(TextToSpeech.audio))

    def nightcore(self, sample,sr):
        return pyrb.time_stretch(np.asarray(sample), sr,1.2)

    def try_fishspeak(self, prompt):
        if(not self.curr_playing):
            self.fishspeak(prompt)

    def fishspeak(self, prompt):
        self.curr_playing = True
        array = self.tts.tts(text=prompt, speaker=self.tts.speakers[17])
        # array = self.nightcore(array, 22050)
        # print(self.audio)
        # TextToSpeech.curr_playing = True
        # make audio from gpt text
        # thisll take a while, you can do shit as it renders

        # array = self.tts.tts(text=gpt(prompt), speaker=tts.speakers[17])
        # self.audio = self.tts.tts(text=prompt, speaker=self.tts.speakers[17])
        # interesting sounding vctks: 3,13,14,17,
        # 75, 65, 74, 73, 98, 64

        # nightcore
        # array = nightcore(array,22050)

        # start audio
        sd.default.samplerate = 11*22050/10
        sd.play(array)
        status = sd.wait()
        sd.stop()
        self.last_speak = time.time()
        self.curr_playing = False

if __name__ == "__main__":
    tts = TextToSpeech()
    # thread = threading.Thread(target=tts.try_fishspeak, daemon=True)
    # thread.start()
    # tts.fishspeak("Can you laugh?")
    # tts.fishspeak("Can you laugh?")
    time.sleep(5)
    # sd.play(tts.tts(text="Check the manual build section if you wish to compile the bindings from source to enable additional modules such as CUDA.", speaker=tts.speakers[3]), 22050)
    status = sd.wait()
    sd.stop()
