import kivy
kivy.require('1.0.6')
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition


Builder.load_string("""
<WelcomeScreen>:
    Image:
        source: 'LogoDark.png'
        size: self.texture_size
<MenuScreen>:
    Image:
        source: 'LogoDark.png'
        size: self.texture_size
        size_hint_x: 1
        size_hint_y: 1.50
    Button:
        text: 'Start'
        size: 100, 40
        size_hint: None, None
        pos: 350, 320

    Button:
        text: 'Settings'
        size: 100, 40
        size_hint: None, None
        pos: 350, 250

    Button:
        text: 'Close'
        size: 100, 40
        size_hint: None, None
        pos: 350, 180

""")


# Declare both screens
class EmptyScreen1(Screen):
    def switch(self, *args):
        self.parent.current = "welcome"

    def on_enter(self, *args):
        # called when this Screen is displayed
        Clock.schedule_once(self.switch, 2)

class EmptyScreen2(Screen):
    def switch(self, *args):
        self.parent.current = "menu"

    def on_enter(self, *args):
        # called when this Screen is displayed
        Clock.schedule_once(self.switch, 2)

class WelcomeScreen(Screen):
    def switch(self, *args):
        self.parent.current = "Empty2"

    def on_enter(self, *args):
        # called when this Screen is displayed
        Clock.schedule_once(self.switch, 2)

class MenuScreen(Screen):
    pass




# Create the screen manager
sm = ScreenManager(transition=FadeTransition())
sm.add_widget(EmptyScreen1(name='Empty1'))
sm.add_widget(EmptyScreen2(name='Empty2'))
sm.add_widget(WelcomeScreen(name='welcome'))
sm.add_widget(MenuScreen(name='menu'))
class TestApp(App):

    def build(self):
        return sm

if __name__ == '__main__':
    TestApp().run()