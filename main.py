from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.relativelayout import RelativeLayout

from sound_kit_service import SoundKitService
from track import TrackWidget

Builder.load_file("track.kv")


class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound_kit_service = SoundKitService()

    def on_parent(self, widget, parent):
        for i in range(0, self.sound_kit_service.get_nb_tracks()):
            sound_i = self.sound_kit_service.get_sound_at(i)
            self.tracks_layout.add_widget(TrackWidget(sound_i))


class MrBeatApp(App):
    pass


MrBeatApp().run()
