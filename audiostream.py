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
            
            
class FeedAudioStream(Audiostream):
    
    def __init__(self, keep_open=False, volume_prio=1):
        Audiostream.__init__(self, volume_prio)
        self.keep_open = keep_open
        self.closed = False
        self.data = []
        self.offset = 0
        
    def feed(self, data):
        if self.closed:
            print("WARNING: Trying to add data to a closed stream.")
        self.data.append(data)
        
    def clean(self):
        self.data = self.data[self.offset:]
        self.offset = 0
        
    def get_data(self, frame_count, channels, width, rate, format):
        size = min(len(self.data)-self.offset, frame_count*channels)
        if size == 0 and not self.keep_open:
            self.closed = True
            return None
        data = numpy.array(self.data[self.offset:self.offset+size])
        self.offset += size
        if self.offset > rate:
            self.clean()
        return data
            