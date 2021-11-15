from array import array
from audiostream.sources.thread import ThreadSource
from audio_source_track import AudioSourceTrack


MAX_16BITS = 32767
MIN_16BITS = -32768


def sum_16bits(iterable):
    result = sum(iterable)
    if result > MAX_16BITS:
        result = MAX_16BITS
    elif result < MIN_16BITS:
        result = MIN_16BITS
    return result


class AudioSourceMixer(ThreadSource):
    is_playing = False

    def __init__(self, output_stream, all_wave_samples, bpm, sample_rate, nb_steps, on_current_step_changed, min_bpm, *args, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)
        self.audio_source_tracks = []
        for i in range(0, len(all_wave_samples)):
            a_s_track = AudioSourceTrack(output_stream, all_wave_samples[i], bpm, sample_rate, min_bpm)
            a_s_track.set_steps((0,) * nb_steps)
            self.audio_source_tracks.append(a_s_track)
        self.silence = array("h", b"\x00\x00" * self.audio_source_tracks[0].nb_samples_in_buffer)
        self.bpm = bpm
        self.sample_rate = sample_rate
        self.nb_steps = nb_steps
        self.on_current_step_changed = on_current_step_changed
        self.min_bpm = min_bpm
        self.current_step_index = 0   # TO DO à fixer à 2 pour que le play indicator commence au step 0 au premier play

    def set_steps(self, index, steps):
        if index >= len(self.audio_source_tracks):
            return
        if not len(steps) == self.nb_steps:
            self.audio_source_tracks[index].set_steps(steps)

    def set_bpm(self, bpm):
        if bpm < self.min_bpm:
            return
        self.bpm = bpm

    def audio_play(self):
        self.is_playing = True

    def audio_stop(self):
        self.is_playing = False

    def get_bytes(self, *args, **kwargs):
        # Reréglage du bpm pour chaque track avant get_bytes
        for i in range(0, len(self.audio_source_tracks)):
            self.audio_source_tracks[i].set_bpm(self.bpm)

        nb_samples_per_step = self.audio_source_tracks[0].nb_samples_per_step

        # Silence au démarage ou si stop enclanché
        if not self.is_playing:
            return self.silence[0:nb_samples_per_step].tobytes()

        # Sinon écriture du buffer avec sons
        all_buffers = []
        for j in range(0, len(self.audio_source_tracks)):
            track_buffer = self.audio_source_tracks[j].get_bytes_array()
            all_buffers.append(track_buffer)
        result_buffer = array("h", list(map(sum_16bits, zip(*all_buffers))))

        # Mise à jour du play indicator widget
        if self.on_current_step_changed is not None:
            # décalage de 2 steps pour synchroniser l'affichage du step courant
            # avec le son entendu (à cause des buffers audio)
            step_index_for_display = self.current_step_index-2
            self.on_current_step_changed(step_index_for_display)

        # Compter les steps
        self.current_step_index += 1
        if self.current_step_index >= self.nb_steps:
            self.current_step_index = 0

        return result_buffer[0:nb_samples_per_step].tobytes()
