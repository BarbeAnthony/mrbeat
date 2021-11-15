from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import ObjectProperty, Clock, NumericProperty
from kivy.uix.relativelayout import RelativeLayout
from audio_engine import AudioEngine
from sound_kit_service import SoundKitService
from track import TrackWidget

Builder.load_file("track.kv")
Builder.load_file("play_indicator.kv")

NB_STEP_BUTTON = 16
SOUND_BUTTON_WIDTH = dp(100)

# /!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\
# /!\   TO DO ctrl+F "compensation de bug" à régler avant déploiement  /!\
# /!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\/!\

class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty()
    play_indicator_widget = ObjectProperty()
    bpm = NumericProperty(60)
    current_step_index = 0

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound_kit_service = SoundKitService()
        # kick_sound = self.sound_kit_service.get_sound_at(0)
        self.audio_engine = AudioEngine()
        # self.audioengine.play_sound(kick_sound.samples)
        # self.audio_engine.create_track(kick_sound.samples, 60)
        all_wave_samples = self.sound_kit_service.get_all_samples()
        self.audio_source_mixer = self.audio_engine.create_mixer(all_wave_samples, 60, NB_STEP_BUTTON, self.on_mixer_current_step_changed)   # compensation de bug, valeur souhaitée 120bpm

    def on_parent(self, widget, parent):
        self.play_indicator_widget.set_nb_steps_and_position(NB_STEP_BUTTON, SOUND_BUTTON_WIDTH)
        for i in range(0, self.sound_kit_service.get_nb_tracks()):
            sound_i = self.sound_kit_service.get_sound_at(i)
            audio_source_track_i = self.audio_source_mixer.audio_source_tracks[i]
            self.tracks_layout.add_widget(TrackWidget(self.audio_engine, sound_i, NB_STEP_BUTTON, audio_source_track_i, SOUND_BUTTON_WIDTH))

    def on_mixer_current_step_changed(self, current_step_index):
        self.current_step_index = current_step_index
        Clock.schedule_once(self.on_update_play_indicator_cbk, 0)

    def on_update_play_indicator_cbk(self, dt):
        if self.play_indicator_widget is not None:
            self.play_indicator_widget.set_step_display_at_index(self.current_step_index)

    def on_play_button_pressed(self):
        self.audio_source_mixer.audio_play()

    def on_stop_button_pressed(self):
        self.audio_source_mixer.audio_stop()

    def on_bpm(self, widget, value):
        if value > 160:
            self.bpm = 160
            # return pour éviter un double appel de la fin de on_bpm, car la fonction boucle sur elle même
            return
        elif value < 60:
            self.bpm = 60
            return



class MrBeatApp(App):
    pass


MrBeatApp().run()
