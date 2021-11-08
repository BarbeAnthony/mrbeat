from kivy.uix.boxlayout import BoxLayout
from kivy.uix.togglebutton import ToggleButton

NB_STEP_BUTTON = 16


class TrackWidget(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        for i in range(0, NB_STEP_BUTTON):
            self.add_widget(TrackStepButton())


class TrackStepButton(ToggleButton):
    pass
