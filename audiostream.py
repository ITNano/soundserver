import numpy
import wave
        
class Audiostream(object):
    
    def __init__(self, volume_prio=1):
        self.volume_prio = volume_prio
        
    def get_data(self, frame_count, channels, width, rate):
        return "".join(["\x00"]*frames*self.channels*self.width)
        
    def get_volume_priority(self):
        return self.volume_prio
        
        
class WaveAudioStream(Audiostream):
    
    def __init__(self, file, volume_prio=1):
        Audiostream.__init__(self, volume_prio)
        self.wf = wave.open(file)
        
    def get_data(self, frame_count, channels, width, rate, format):
        data = self.wf.readframes(frame_count)
        if len(data) > 0:
            return numpy.fromstring(data, format)
        else:
            return None