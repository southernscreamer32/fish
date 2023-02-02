import sounddevice as sd
from TTS.api import TTS
import soundfile as sf
import numpy as np

# tts = TTS("tts_models/en/vctk/vits", gpu=False)


def fishspeak():

    # make audio from gpt text
    # thisll take a while, you can do shit as it renders
    # tts.tts_to_file(text="Warning: By default, the volume is set to zero because it is not possible to determine how loud the sound will be when played.", speaker=tts.speakers[17], file_path='out.wav')

    # interesting sounding vctks: 3,13,14,17,
    # 75, 65, 74, 73, 98, 64

    # nightcore
    # array = nightcore(array,22050)

    # sd.default.device = 'Speakers (Razer Kraken Kitty Edition), Windows WDM-KS'

    array,fs = sf.read('gui/out.wav', dtype='float64')

    # start audio
    sd.play(array,fs)
    status = sd.wait()
    sd.stop()

if __name__ == "__main__":
    fishspeak()