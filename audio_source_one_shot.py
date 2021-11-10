from array import array
from audiostream.sources.thread import ThreadSource


class AudioSourceOneShot(ThreadSource):
    def __init__(self, output_stream, *args, **kwargs):
        super().__init__(self, output_stream, *args, **kwargs)
        self.nb_samples_in_chunk = 32
        self.buffer = array("h", b"\x00\x00" * self.nb_samples_in_chunk)

    def get_bytes(self, *args, **kwargs):
        return self.buffer.tobytes()
