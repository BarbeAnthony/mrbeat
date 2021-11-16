from kivy.metrics import dp
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.image import Image
from kivy.uix.togglebutton import ToggleButton


class TrackWidget(BoxLayout):
    def __init__(self, audio_engine, sound, nb_step_button, track_source, left_part_of_track_width, **kwargs):
        super().__init__(**kwargs)
        self.audio_engine = audio_engine
        self.sound = sound
        self.nb_step_button = nb_step_button
        self.track_source = track_source
        # self.track_audio_source = self.audio_engine.create_track(self.sound.samples, 60)

        # BoxLayout for sound button and separator
        sound_button_and_separator = BoxLayout()
        sound_button_and_separator.size_hint_x = None
        sound_button_and_separator.width = left_part_of_track_width
        self.add_widget(sound_button_and_separator)

        # Sound button -> BoxLayout
        sound_button = TrackSoundButton()
        sound_button.text = sound.displayname
        sound_button.on_press = self.on_sound_button_press
        sound_button_and_separator.add_widget(sound_button)

        # Separator -> BoxLayout
        separator = Image(source="images/track_separator.png")
        separator.size_hint_x = None
        separator.width = dp(15)
        sound_button_and_separator.add_widget(separator)

        # Step buttons
        self.step_buttons = []
        for i in range(0, nb_step_button):
            step_button = TrackStepButton()
            step_button.bind(state=self.on_step_button_state)
            # alterner 4 boutons avec background step_normal1.png et 4 boutons avec background step_normal2.png
            if (i // 4) % 2 == 1:
                step_button.background_normal = "images/step_normal2.png"
            self.step_buttons.append(step_button)
            self.add_widget(step_button)

    def on_sound_button_press(self):
        self.audio_engine.play_sound(self.sound.samples)

    def on_step_button_state(self, widget, state):
        steps = []
        for i in range(0, self.nb_step_button):
            if self.step_buttons[i].state == "down":
                steps.append(1)
            else:
                steps.append(0)
        # self.track_audio_source.set_steps(steps)
        self.track_source.set_steps(steps)

    def set_step_buttons_normal(self):
        for button in self.step_buttons:
            button.state = "normal"


class TrackSoundButton(Button):
    pass


class TrackStepButton(ToggleButton):
    pass
