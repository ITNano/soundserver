import numpy

class Mixer(object):

    def __init__(self, channels=2, width=2, rate=44100):
        self.channels = channels
        self.width = width
        self.rate = rate
        self.format = numpy.int16
        self.streams = []
        
    def get_data(self, frames, time):
        data = numpy.zeros(frames*self.channels)
        if len(self.streams) > 0:
            streams = []
            removed = 0
            for i in range(len(self.streams)):
                index = i-removed
                stream = (self.streams[index].get_data(frames, self.channels, self.width, self.rate, self.format), self.streams[index].get_volume_priority())
                if stream[0] is not None:
                    if len(stream[0]) > 0:
                        streams.append(stream)
                else:
                    self.streams.pop(index)
                    removed += 1
                    
            if len(streams) > 0:
                base_factor = 1/len(streams)
                for (stream, prio) in streams:
                    if len(stream) < len(data):
                        stream = numpy.pad(stream, pad_width=(0, frames*self.channels-len(stream)), mode="constant", constant_values=0)
                    data = data + stream*(base_factor*prio)
        return data.astype(self.format).tostring()
        
    def add_sound(self, audiostream):
        self.streams.append(audiostream)
        
    def close(self):
        pass
        