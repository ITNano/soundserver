import sound
import time
import audiostream

s = sound.Sound()
s.add_sound(2, audiostream.WaveAudioStream("test.wav", 0.5))
s.start_streams()

time.sleep(2)

s.add_sound(2, audiostream.WaveAudioStream("bering.wav", 2))
s.add_sound(2, audiostream.FeedAudioStream(keep_open=True))

time.sleep(10)

s.stop_streams()
s.terminate()