from array import array
from audiostream.sources.thread import ThreadSource


class AudioSourceTrack(ThreadSource):
    steps = ()
    nb_samples_per_step = 0
    buffer = None

    def __init__(self, output_stream, wave_samples, bpm, sample_rate,  *args, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)
        self.wave_samples = wave_samples
        self.nb_wave_samples = len(wave_samples)
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.current_sample_index = 0
        self.current_step_index = 0
        self.compute_nb_samples_per_step_and_alloc_buffer()

    def set_steps(self, steps):
        if not len(steps) == len(self.steps):
            self.current_step_index = 0
        self.steps = steps

    def set_bpm(self, bpm):
        self.bpm = bpm
        self.compute_nb_samples_per_step()

    def compute_nb_samples_per_step_and_alloc_buffer(self):
        if not self.bpm == 0:
            new_nb_samples_per_step = int(self.sample_rate * 60 / (4 * self.bpm))   # 60s par minute, 4 steps par battement
            if not new_nb_samples_per_step == self.nb_samples_per_step:
                self.nb_samples_per_step = new_nb_samples_per_step
                self.buffer = array("h", b"\x00\x00" * self.nb_samples_per_step)   # nb samples per chunk = nb_samples_per_step

    def get_bytes(self, *args, **kwargs):
        for i in range(0, self.nb_samples_per_step):
            if len(self.steps) > 0:
                if self.steps[self.current_step_index] == 1 and i < self.nb_wave_samples:
                    self.buffer[i] = self.wave_samples[i]
                    if i == 0:
                        self.current_sample_index = 0
                else:
                    if 0 < self.current_sample_index < self.nb_wave_samples:
                        self.buffer[i] = self.wave_samples[self.current_sample_index]
                    else:
                        self.buffer[i] = 0
            else:
                self.buffer[i] = 0
            self.current_sample_index += 1
        self.current_step_index += 1
        if self.current_step_index >= len(self.steps):
            self.current_step_index = 0
        return self.buffer.tobytes()

