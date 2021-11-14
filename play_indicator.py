from kivy.metrics import dp
from kivy.properties import NumericProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.togglebutton import ToggleButton


class PlayIndicatorButton(ToggleButton):
    pass


class PlayIndicatorWidget(BoxLayout):
    nb_steps = 0
    play_indicator_buttons = []

    def set_nb_steps_and_position(self, nb_steps, place_holder_button_width):
        if not nb_steps == self.nb_steps:
            self.nb_steps = nb_steps
            self.play_indicator_buttons = []
            self.clear_widgets()

            place_holder_button = Button()
            place_holder_button.size_hint_x = None
            place_holder_button.width = place_holder_button_width
            self.add_widget(place_holder_button)

            for i in range(0, nb_steps):
                button = PlayIndicatorButton()
                self.play_indicator_buttons.append(button)
                self.add_widget(button)
