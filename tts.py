import openai
import sounddevice as sd
from TTS.api import TTS
import librosa as lr
import numpy as np
import pyrubberband as pyrb

openai.api_key = "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"
tts = TTS("tts_models/en/vctk/vits", gpu=False)


def nightcore(sample,sr):
    return pyrb.time_stretch(np.asarray(sample), sr, 2.0)

def gpt(prompt):
    completion = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"You are a Blue Tilapia in an aquarium, and I am having a conversation with you. {prompt}",
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    return completion.choices[0].text

def fishspeak(prompt):
    # make audio from gpt text
    # thisll take a while, you can do shit as it renders

    array = tts.tts(text=gpt(prompt), speaker=tts.speakers[17])

    # interesting sounding vctks: 3,13,14,17,
    # 75, 65, 74, 73, 98, 64

    # nightcore
    # array = nightcore(array,22050)

    # start audio
    sd.play(array, 22050)
    status = sd.wait()
    sd.stop()

if __name__ == "__main__":
    fishspeak("Can you laugh?")
    # sd.play(tts.tts(text="Check the manual build section if you wish to compile the bindings from source to enable additional modules such as CUDA.", speaker=tts.speakers[3]), 22050)
    # status = sd.wait()
    # sd.stop()