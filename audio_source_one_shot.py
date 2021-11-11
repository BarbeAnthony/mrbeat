from array import array
from audiostream.sources.thread import ThreadSource


class AudioSourceOneShot(ThreadSource):
    wave_samples = None
    nb_wave_samples = 0

    def __init__(self, output_stream, *args, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)
        self.nb_samples_per_chunk = 32
        self.current_sample_index = 0
        self.buffer = array("h", b"\x00\x00" * self.nb_samples_per_chunk)

    def get_bytes(self, *args, **kwargs):
        if self.nb_wave_samples > 0:
            for i in range(0, self.nb_samples_per_chunk):
                if self.current_sample_index < self.nb_wave_samples:
                    self.buffer[i] = self.wave_samples[self.current_sample_index]
                else:
                    self.buffer[i] = 0
                self.current_sample_index += 1
        return self.buffer.tobytes()

    def set_wave_samples(self, wave_samples):
        self.wave_samples = wave_samples
        self.current_sample_index = 0
        self.nb_wave_samples = len(wave_samples)
