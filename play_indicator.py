from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.widget import Widget


class PlayIndicatorLight(Image):
    pass


class PlayIndicatorWidget(BoxLayout):
    nb_steps = 0
    play_indicator_lights = []

    def set_step_display_at_index(self, index):
        if index < self.nb_steps:
            for light in self.play_indicator_lights:
                light.source = "images/indicator_light_off.png"
            self.play_indicator_lights[index].source = "images/indicator_light_on.png"

    def set_nb_steps_and_position(self, nb_steps, place_holder_widget_width):
        if not nb_steps == self.nb_steps:
            self.nb_steps = nb_steps
            self.play_indicator_lights = []
            self.clear_widgets()

            # décalage des PlayIndicatorLights pour alignement avec les TrackStepButtons
            place_holder_widget = Widget()
            place_holder_widget.size_hint_x = None
            place_holder_widget.width = place_holder_widget_width
            self.add_widget(place_holder_widget)

            for i in range(0, nb_steps):
                light = PlayIndicatorLight()
                light.source = "images/indicator_light_off.png"
                self.play_indicator_lights.append(light)
                self.add_widget(light)
