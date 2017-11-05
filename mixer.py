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
            base_factor = 1/len(self.streams)
            remove = []
            for i in range(len(self.streams)):
                stream_data = self.streams[i].get_data(frames, self.channels, self.width, self.rate, self.format)
                if stream_data is not None:
                    if len(stream_data) < len(data):
                        stream_data = numpy.pad(stream_data, pad_width=(0, frames*self.channels-len(stream_data)), mode="constant", constant_values=0)
                    data = data + stream_data*(base_factor*self.streams[i].get_volume_priority())
                else:
                    remove.append(i)
            if len(remove) > 0:
                for i in remove:
                    self.streams.pop(i)
        return data.astype(self.format).tostring()
        
    def add_sound(self, audiostream):
        self.streams.append(audiostream)
        
    def close(self):
        pass
        