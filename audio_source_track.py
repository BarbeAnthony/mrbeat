from array import array
from audiostream.sources.thread import ThreadSource


class AudioSourceTrack(ThreadSource):
    steps = ()
    nb_samples_per_step = 0
    buffer = None

    def __init__(self, output_stream, wave_samples, bpm, sample_rate, min_bpm,  *args, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)
        self.wave_samples = wave_samples
        self.nb_wave_samples = len(wave_samples)
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.min_bpm = min_bpm
        # FIX : valeur initiale pour éviter son joué au démarage
        self.current_sample_index = self.nb_wave_samples
        self.current_step_index = 0
        self.nb_samples_per_step = self.compute_nb_samples_per_step(bpm)
        # allocation du buffer à sa taille max, pour qu'il puisse gérer tous les cas
        self.nb_samples_in_buffer = self.compute_nb_samples_per_step(min_bpm)
        self.buffer = array("h", b"\x00\x00" * self.nb_samples_in_buffer)

    def set_steps(self, steps):
        if not len(steps) == len(self.steps):
            self.current_step_index = 0
        self.steps = steps

    def set_bpm(self, bpm):
        self.bpm = bpm
        self.nb_samples_per_step = self.compute_nb_samples_per_step(bpm)

    def compute_nb_samples_per_step(self, bpm):
        if not bpm == 0:
            new_nb_samples_per_step = int(self.sample_rate * 60 / (4 * bpm))   # 60s par minute, 4 steps par battement
            return new_nb_samples_per_step
        return 0

    def get_bytes_array(self,):
        for i in range(0, self.nb_samples_per_step):
            if len(self.steps) > 0:
                if self.steps[self.current_step_index] == 1 and i < self.nb_wave_samples:
                    self.buffer[i] = self.wave_samples[i]
                    if i == 0:
                        self.current_sample_index = 0
                else:
                    if self.current_sample_index < self.nb_wave_samples:
                        self.buffer[i] = self.wave_samples[self.current_sample_index]
                    else:
                        self.buffer[i] = 0
            else:
                self.buffer[i] = 0
            self.current_sample_index += 1
        self.current_step_index += 1
        if self.current_step_index >= len(self.steps):
            self.current_step_index = 0
        return self.buffer[0:self.nb_samples_per_step]

    def get_bytes(self, *args, **kwargs):
        return self.get_bytes_array().tobytes()
