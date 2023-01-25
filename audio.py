import sounddevice as sd
import threading

class Audio:
    def __init__(self):
        self.currently_playing = False
        self.audio_stream = sd.OutputStream(samplerate=44100, device=self.output_device, channels=2,
        finished_callback=self.set_true)    #can't be bothered to lambda
        self.output_device = 3
    
    def set_true(self):
        self.currently_playing = True

    def play_audio(self, audio_data):
        self.currently_playing = True
        self.audio_stream.write(audio_data)


    def callback(self):
        pass