from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.relativelayout import RelativeLayout

from sound_kit_service import SoundKitService
from track import TrackWidget

Builder.load_file("track.kv")

NB_TRACKS = 4


class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.sound_kit_service = SoundKitService()

    def on_parent(self, widget, parent):
        for i in range(0, NB_TRACKS):
            self.tracks_layout.add_widget(TrackWidget())


class MrBeatApp(App):
    pass


MrBeatApp().run()
