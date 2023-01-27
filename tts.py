import openai
import sounddevice as sd
from TTS.api import TTS
import numpy as np
import pyrubberband as pyrb
import queue, threading, time

openai.api_key = ""
class TextToSpeech():
    # text to speech handlesdropping 
    # curr_playing = False
    audio = []
    def __init__(self):
        self.tts = TTS("tts_models/en/vctk/vits", gpu=True)
        
        self.speak_queue = queue.Queue()
        
        # audio stuff
        self.curr_playing = False
        self.delay = 1  #delay in secs before saying something new
        self.last_speak = time.process_time()

        self.audio = []
        devices = sd.query_devices()
        print(devices)
        self.audio_device = sd.default.device[0]
        # print(self.audio_device)
        for device in devices:
            # print(device["name"])
            # print(device)
            if device["name"] == "virtual audio cable": # change name
                self.audio_device = device["index"]
                sd.default.device = device["index"]
                break
        fish_thread = threading.Thread(target=self.try_fishspeak_loop, daemon=True)
        fish_thread.start()
        # sd.default.device
        # print(self.audio_device.name)
        # self.audio_device = sd.query_devices("virtual audio cable") #change name to match actual device name!
        # if self.audio_device:
        #     self.audio_device = self.audio_device[0].name
        # else:
        #     self.audio_device = sd.default.device[1]
        # self.audio_stream = sd.OutputStream(samplerate=22050, device=self.audio_device, channels=2, finished_callback=self.set_audio_false)

    def audio_callback(outdata, frames, time, status):
        print("AAA")
        if TextToSpeech.curr_playing:
            
        # if self.curr_playing:
            outdata[:] = TextToSpeech.audio
            print(len(TextToSpeech.audio))

    def set_audio_false(self):
        self.curr_playing = False

    def nightcore(self, sample,sr):
        return pyrb.time_stretch(np.asarray(sample), sr, 2.0)

    def gpt(prompt):
        completion = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"You are a Blue Tilapia in an aquarium, and I am having a conversation with you. {prompt}",
            max_tokens=1024,
            n=1,
            stop=None,
            temperature=0.9,
            presence_penalty=0.5,
            frequency_penalty=0.5,
        )

        return completion.choices[0].text

    def try_fishspeak(self, prompt):
        self.speak_queue.put(prompt)

    def try_fishspeak_loop(self):
        while True:
            # print("AA")
            # print(self.speak_queue.empty())
            if not self.speak_queue.empty():
                print("A")
                prompt = self.speak_queue.get()
                if time.process_time() - self.last_speak > self.delay and not self.curr_playing:
                        self.fishspeak(prompt)
            time.sleep(0.01)
                

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


        sd.play(array, 22050)
        status = sd.wait()
        sd.stop()
        self.last_speak = time.process_time()
        self.curr_playing = False

if __name__ == "__main__":
    tts = TextToSpeech()
    # thread = threading.Thread(target=tts.try_fishspeak, daemon=True)
    # thread.start()
    time.sleep(1)
    tts.speak_queue.put("can you laugh?")
    time.sleep(6)
    tts.speak_queue.put("can you laugh?")
    # tts.fishspeak("Can you laugh?")
    # tts.fishspeak("Can you laugh?")
    time.sleep(5)
    # sd.play(tts.tts(text="Check the manual build section if you wish to compile the bindings from source to enable additional modules such as CUDA.", speaker=tts.speakers[3]), 22050)
    status = sd.wait()
    sd.stop()
