from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton

NB_STEP_BUTTON = 16


class TrackWidget(BoxLayout):
    def __init__(self, sound, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(TrackSoundButton(text=sound.displayname))
        for i in range(0, NB_STEP_BUTTON):
            self.add_widget(TrackStepButton())


class TrackSoundButton(Button):
    pass


class TrackStepButton(ToggleButton):
    pass
