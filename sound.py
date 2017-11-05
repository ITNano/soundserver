import pyaudio
import numpy as np
import mixer

class Sound(object):

    def __init__(self):
        self.p = pyaudio.PyAudio()
        self.mixers = []
        self.streams = []
        for i in range(self.p.get_device_count()-3):
            self.streams.append(SoundcardStream(self.p, i))
            
    def start_stream(self, index):
        self.streams[index].start_stream()
        
    def start_streams(self):
        for stream in self.streams:
            stream.start_stream()
            
    def add_sound(self, index, sound):
        self.streams[index].add_sound(sound)
            
    def stop_stream(self, index):
        self.streams[index].stop_stream()
            
    def stop_streams(self):
        for stream in self.streams:
            stream.stop_stream()
            
    def terminate(self):
        for stream in self.streams:
            stream.close()
        self.p.terminate()
        
        
class SoundcardStream(object):

    def __init__(self, p, soundcard, width=2, channels=2, rate=44100):
        self.soundcard = soundcard
        self.mixer = mixer.Mixer(width, channels, rate)
        try:
            print("Loading soundcard "+str(soundcard))
            self.stream = p.open(format=p.get_format_from_width(width), channels=channels, rate=rate, output_device_index=soundcard, output=True, stream_callback=self.get_data)
        except:
            self.stream = None
            print("Device unavailable (index "+str(soundcard)+")")
        
    def get_data(self, in_data, frame_count, time_info, status):
        return (self.mixer.get_data(frame_count, time_info["input_buffer_adc_time"]), pyaudio.paContinue)
        
    def add_sound(self, sound):
        print("Adding sound to soundcard "+str(self.soundcard))
        self.mixer.add_sound(sound)
        
    def start_stream(self):
        if self.stream is not None:
            self.stream.start_stream()
        
    def stop_stream(self):
        if self.stream is not None:
            self.stream.stop_stream()
        
    def close(self):
        if self.stream is not None:
            self.stream.close()
        self.mixer.close()