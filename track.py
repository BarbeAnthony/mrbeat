from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

NB_STEP_BUTTON = 16


class TrackWidget(BoxLayout):
    def __init__(self, audio_engine, sound_in_track, **kwargs):
        super().__init__(**kwargs)
        self.audio_engine = audio_engine
        self.sound_in_track = sound_in_track
        sound_button = TrackSoundButton()
        sound_button.text = sound_in_track.displayname
        sound_button.on_press = self.on_sound_button_press
        self.add_widget(sound_button)
        for i in range(0, NB_STEP_BUTTON):
            self.add_widget(TrackStepButton())

    def on_sound_button_press(self):
        self.audio_engine.play_sound(self.sound_in_track.samples)


class TrackSoundButton(Button):
    pass


class TrackStepButton(ToggleButton):
    pass
