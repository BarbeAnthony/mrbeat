from kivy.app import App
from kivy.lang import Builder
from kivy.properties import ObjectProperty
from kivy.uix.relativelayout import RelativeLayout
from track import TrackWidget

Builder.load_file("track.kv")

NB_TRACKS = 4


class MainWidget(RelativeLayout):
    tracks_layout = ObjectProperty(None)

    def on_parent(self, widget, parent):
        for i in range(0, NB_TRACKS):
            self.tracks_layout.add_widget(TrackWidget())


class MrBeatApp(App):
    pass


MrBeatApp().run()
