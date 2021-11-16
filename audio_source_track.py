from array import array
from audiostream.sources.thread import ThreadSource


class AudioSourceTrack(ThreadSource):
    steps = ()
    nb_samples_per_step = 0

    def __init__(self, output_stream, wave_samples, bpm, sample_rate, min_bpm,  *args, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)
        self.wave_samples = wave_samples
        self.nb_wave_samples = len(wave_samples)
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.min_bpm = min_bpm
        self.current_sample_index = 0
        self.current_step_index = 0
        self.nb_samples_per_step = self.compute_nb_samples_per_step(bpm)
        # allocation du buffer à sa taille max, pour qu'il puisse gérer tous les cas
        self.nb_samples_in_buffer = self.compute_nb_samples_per_step(min_bpm)
        self.silence = array("h", b"\x00\x00" * self.nb_samples_in_buffer)

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

    def no_step_activated(self):
        if len(self.steps) == 0:
            return True
        for step in self.steps:
            if step == 1:
                return False
        return True

    def get_bytes_array(self,):
        result_buffer = None

        # 1 : aucun step activé et pas de son commencé-> silence
        if self.no_step_activated():
            result_buffer = self.silence[0:self.nb_samples_per_step]
            self.current_sample_index = 0
        # 2 : step activé -> jouer du son
        elif self.steps[self.current_step_index] == 1:
            # 2.1 : le son a plus ou autant de samples qu'un step -> remplir le buffer avec les samples du son son
            if self.nb_wave_samples >= self.nb_samples_per_step:
                result_buffer = self.wave_samples[0:self.nb_samples_per_step]
                self.current_sample_index = self.nb_samples_per_step
            # 2.2 : le son a moins de samples qu'un step -> remplir le buffer avec les samples du son et compléter avec du silence
            else:
                silence_nb_samples = self.nb_samples_per_step - self.nb_wave_samples
                result_buffer = self.wave_samples[0:self.nb_wave_samples]
                result_buffer.extend(self.silence[0:silence_nb_samples])
                self.current_sample_index = 0
        # 3 : step désactivé
        else:
            # 3.1 : il reste du son à jouer du step précédent
            if self.current_sample_index > 0:
                nb_remaining_wave_samples = self.nb_wave_samples - self.current_sample_index
                # 3.1.1 : la fin du son a plus ou autant de samples qu'un step -> remplir le buffer avec le son
                if nb_remaining_wave_samples >= self.nb_samples_per_step:
                    result_buffer = self.wave_samples[self.current_sample_index:self.current_sample_index + self.nb_samples_per_step]
                    self.current_sample_index += self.nb_samples_per_step
                # 3.1.2 : la fin du son a moins de samples qu'un step -> remplir le buffer avec les samples restants et complléter avec du silence
                else:
                    silence_nb_samples = self.nb_samples_per_step - nb_remaining_wave_samples
                    result_buffer = self.wave_samples[self.current_sample_index:self.current_sample_index + nb_remaining_wave_samples]
                    result_buffer.extend(self.silence[0:silence_nb_samples])
                    self.current_sample_index = 0
            # 3.2 : pas de son à jouer du step précédent -> silence
            else:
                result_buffer = self.silence[0:self.nb_samples_per_step]

        self.current_step_index += 1
        if self.current_step_index >= len(self.steps):
            self.current_step_index = 0

        if result_buffer is None:
            print("result_buffer is None")
        elif not len(result_buffer) == self.nb_samples_per_step:
            print("result_buffer length is not nb_samples_per_step")

        return result_buffer

    def get_bytes(self, *args, **kwargs):
        return self.get_bytes_array().tobytes()
