from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.relativelayout import RelativeLayout
from audio_engine import AudioEngine
from sound_kit_service import SoundKitService
from track import TrackWidget

Builder.load_file("track.kv")

NB_STEP_BUTTON = 16


class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound_kit_service = SoundKitService()
        # kick_sound = self.sound_kit_service.get_sound_at(0)
        self.audio_engine = AudioEngine()
        # self.audioengine.play_sound(kick_sound.samples)
        # self.audio_engine.create_track(kick_sound.samples, 60)
        all_wave_samples = self.sound_kit_service.get_all_samples()
        self.audio_engine.create_mixer(all_wave_samples, 60, NB_STEP_BUTTON)

    def on_parent(self, widget, parent):
        for i in range(0, self.sound_kit_service.get_nb_tracks()):
            sound_i = self.sound_kit_service.get_sound_at(i)
            self.tracks_layout.add_widget(TrackWidget(self.audio_engine, sound_i, NB_STEP_BUTTON))


class MrBeatApp(App):
    pass


MrBeatApp().run()
