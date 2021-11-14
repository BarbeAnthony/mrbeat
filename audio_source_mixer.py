from array import array
from audiostream.sources.thread import ThreadSource

from audio_source_track import AudioSourceTrack


class AudioSourceMixer(ThreadSource):
    buffer = None

    def __init__(self, output_stream, all_wave_samples, bpm, sample_rate, nb_steps, on_current_step_changed, *args, **kwargs):
        ThreadSource.__init__(self, output_stream, *args, **kwargs)
        self.audio_source_tracks = []
        for i in range(0, len(all_wave_samples)):
            a_s_track = AudioSourceTrack(output_stream, all_wave_samples[i], bpm, sample_rate)
            a_s_track.set_steps((0,) * nb_steps)
            self.audio_source_tracks.append(a_s_track)
        self.sample_rate = sample_rate
        self.nb_steps = nb_steps
        self.on_current_step_changed = on_current_step_changed
        # self.current_sample_index = 0
        self.current_step_index = 0

    def set_steps(self, index, steps):
        if index >= len(self.audio_source_tracks):
            return
        if not len(steps) == self.nb_steps:
            self.audio_source_tracks[index].set_steps(steps)

    def set_bpm(self, bpm):
        for i in range(0, len(self.audio_source_tracks)):
            self.audio_source_tracks[i].set_bpm(bpm)

    def get_bytes(self, *args, **kwargs):
        nb_samples_per_step = self.audio_source_tracks[0].nb_samples_per_step
        if self.buffer is None or not len(self.buffer) == nb_samples_per_step:
            self.buffer = array("h", b"\x00\x00" * nb_samples_per_step)
        all_buffers = []
        for j in range(0, len(self.audio_source_tracks)):
            track_buffer = self.audio_source_tracks[j].get_bytes_array()
            all_buffers.append(track_buffer)
        for i in range(0, nb_samples_per_step):
            self.buffer[i] = 0
            for j in range(0, len(all_buffers)):
                self.buffer[i] += all_buffers[j][i]
            # self.current_sample_index += 1
        if self.on_current_step_changed is not None:
            # décalage de 2 steps pour synchroniser l'affichage du step courant
            # avec le son entendu (à cause des buffers audio)
            step_index_for_display = self.current_step_index-2
            self.on_current_step_changed(step_index_for_display)
        self.current_step_index += 1
        if self.current_step_index >= self.nb_steps:
            self.current_step_index = 0
        return self.buffer.tobytes()
