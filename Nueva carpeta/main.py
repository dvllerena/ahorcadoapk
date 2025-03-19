import os
import random
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivy.uix.image import Image
from kivy.clock import Clock
from kivymd.uix.button import MDIconButton
from kivy.core.audio import SoundLoader
from kivymd.uix.button import MDIconButton, MDButton, MDButtonText
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.animation import Animation
from kivy.uix.effectwidget import EffectWidget
from kivy.graphics import Color, Rectangle
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog
from datetime import datetime, date
from kivy.uix.relativelayout import RelativeLayout
from kivymd.uix.button import MDButton
class SplashScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.switch_to_main, 3)

    def switch_to_main(self, dt):
        self.manager.transition.direction = 'left'
        self.manager.current = 'main'

class MainScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.music_player = self.create_music_player()
        self.countdown_label = MDLabel(text="", halign="center")
        self.romantic_message_label = MDLabel(text="", halign="center")
       



        
        layout = MDBoxLayout(orientation='vertical')
        layout.add_widget(self.music_player)
        layout.add_widget(self.countdown_label)
        layout.add_widget(self.romantic_message_label)
        
        self.add_widget(layout)
        
        Clock.schedule_interval(self.update_countdown, 1)

    def create_music_player(self):
        player = MDBoxLayout(orientation='horizontal', size_hint=(1, 0.1), pos_hint={'top': 1})
        self.play_pause_button = MDIconButton(icon="play")
        self.play_pause_button.bind(on_release=self.toggle_play_pause)
        self.next_button = MDIconButton(icon="skip-next")
        self.next_button.bind(on_release=self.play_next_song)
        self.song_label = MDLabel(text="Now playing: ")
        
        player.add_widget(self.play_pause_button)
        player.add_widget(self.next_button)
        player.add_widget(self.song_label)
        
        return player

    def toggle_play_pause(self, instance):
        app = MDApp.get_running_app()
        if app.current_song:
            if app.current_song.state == 'play':
                app.current_song.stop()
                self.play_pause_button.icon = "play"
            else:
                app.current_song.play()
                self.play_pause_button.icon = "pause"

    def play_next_song(self, instance):
        app = MDApp.get_running_app()
        app.play_next_song()
        self.update_song_label()

    def update_song_label(self):
        app = MDApp.get_running_app()
        if app.current_song:
            self.song_label.text = f"Now playing: {os.path.basename(app.current_song.source)}"

    def update_countdown(self, dt):
        next_anniversary = date(date.today().year, 7, 31)  # Ajusta esta fecha a tu aniversario
        if next_anniversary < date.today():
            next_anniversary = date(date.today().year + 1, 7, 31)
        days_left = (next_anniversary - date.today()).days
        self.countdown_label.text = f"Faltan {days_left} días para nuestro próximo aniversario"

    def generate_romantic_message(self, instance=None):
        messages = [
            "Cada día te amo más",
            "Eres mi persona favorita en todo el mundo",
            "Contigo, cada día es una aventura",
            "Tu sonrisa ilumina mi mundo",
            "No puedo imaginar mi vida sin ti"
        ]
        self.romantic_message_label.text = random.choice(messages)


    def on_enter(self):
        self.add_floating_hearts()
        self.update_song_label()

    def add_floating_hearts(self):
        layout = MDFloatLayout()
        for _ in range(10):
            heart = MDIconButton(icon="heart", pos_hint={'x': random.random(), 'y': random.random()})
            layout.add_widget(heart)
            self.animate_heart(heart)
        self.add_widget(layout)

    def animate_heart(self, heart):
        anim = Animation(pos_hint={'y': 1}, duration=random.randint(5, 10))
        anim.bind(on_complete=lambda *args: self.reset_heart(heart))
        anim.start(heart)

    def reset_heart(self, heart):
        heart.pos_hint = {'x': random.random(), 'y': -0.1}
        self.animate_heart(heart)

    def go_to_photos(self):
        self.manager.transition.direction = 'left'
        self.manager.current = "photos"

class PhotoScreen(MDScreen):
    def on_enter(self):
        self.load_photos()
        self.start_presentation()

    def load_photos(self):
        photo_dir = "fotos"
        photo_dir_abs = os.path.abspath(photo_dir)
        photo_files = [f for f in os.listdir(photo_dir_abs) if f.lower().endswith('.jpg')]
        
        carousel = self.ids.photo_carousel
        carousel.clear_widgets()
        
        if photo_files:
            for photo_file in photo_files:
                img_path = os.path.join(photo_dir_abs, photo_file)
                
                layout = RelativeLayout()
                img = Image(source=os.path.abspath(img_path), allow_stretch=True, keep_ratio=True)
                layout.add_widget(img)
                carousel.add_widget(layout)
                self.apply_ken_burns_effect(img, layout)
        else:
            self.ids.no_photos_label.opacity = 1

    def apply_ken_burns_effect(self, img, layout):
        img.size = (layout.width * 1.1, layout.height * 1.1)
        img.pos = (-layout.width * 0.05, -layout.height * 0.05)
        
        anim = (Animation(size=(layout.width, layout.height), 
                          pos=(0, 0), 
                          duration=10) + 
                Animation(size=(layout.width * 1.1, layout.height * 1.1), 
                          pos=(-layout.width * 0.05, -layout.height * 0.05), 
                          duration=10))
        anim.repeat = True
        Clock.schedule_once(lambda dt: anim.start(img), 1)

    def start_presentation(self):
        Clock.schedule_interval(self.next_photo, 5)

    def next_photo(self, dt):
        carousel = self.ids.photo_carousel
        carousel.load_next(mode='next')

    def stop_presentation(self):
        Clock.unschedule(self.next_photo)

    def go_back(self):
        self.stop_presentation()
        self.manager.transition.direction = 'right'
        self.manager.current = 'main'

class LockScreen(MDScreen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.questions = [
            ("¿Cuál es la fecha de nuestro aniversario?", "31 de Julio"),
            ("¿Dónde nos besamos por primera vez?", "playa"),
            ("¿cuál es el nombre de la persona que mas tu amas?", "Denny")
        ]
        self.current_question = 0
        self.build_layout()

    def build_layout(self):
        layout = MDBoxLayout(orientation='vertical', spacing=10, padding=20)
        self.question_label = MDLabel(text=self.questions[self.current_question][0], halign="center")
        self.answer_field = MDTextField(hint_text="Tu respuesta")
        submit_button = MDButton()
        button_text= MDButtonText
        button_text.text = "Enviar"
        submit_button.add_widget =button_text
        submit_button.on_release = self.check_answer
        
        layout.add_widget(self.question_label)
        layout.add_widget(self.answer_field)
        layout.add_widget(submit_button)
        self.add_widget(layout)

    
    def check_answer(self, instance=None):
        if self.answer_field.text.lower() == self.questions[self.current_question][1].lower():
            self.current_question += 1
            if self.current_question < len(self.questions):
                self.question_label.text = self.questions[self.current_question][0]
                self.answer_field.text = ""
            else:
                self.manager.transition.direction = 'left'
                self.manager.current = 'main'
        else:
            dialog = MDDialog()
            dialog.text = "Respuesta incorrecta. Inténtalo de nuevo."
            ok_button = MDButton()
            ok_button.text = "OK"
            ok_button.on_release = lambda x: dialog.dismiss()
            dialog.buttons = [ok_button]
            dialog.open()



class AniversarioApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.playlist = []
        self.current_song = None

    def build(self):
        self.theme_cls.primary_palette = "Green"
        self.theme_cls.accent_palette = "Pink"
        self.theme_cls.theme_style = "Light"
        self.theme_cls.primary_hue = "500" 
        self.load_playlist()
        self.play_next_song()
        sm = MDScreenManager()
        sm.add_widget(SplashScreen(name="splash"))
        sm.add_widget(LockScreen(name="lock"))  # Añade la nueva pantalla de bloqueo
        sm.add_widget(MainScreen(name="main"))
        sm.add_widget(PhotoScreen(name="photos"))
        return sm
    def load_playlist(self):
        audio_dir = os.path.join(os.path.dirname(__file__), 'audio')
        self.playlist = [os.path.join(audio_dir, f) for f in os.listdir(audio_dir) if f.endswith('.mp3')]
        random.shuffle(self.playlist)

    def play_next_song(self, dt=None):
        if self.current_song:
            self.current_song.stop()
        if self.playlist:
            next_song = self.playlist.pop(0)
            self.current_song = SoundLoader.load(next_song)
            if self.current_song:
                self.current_song.play()
                Clock.schedule_once(self.play_next_song, self.current_song.length)
            self.playlist.append(next_song)
        else:
            Clock.schedule_once(self.play_next_song, 1)
        
        main_screen = self.root.get_screen('main')
        main_screen.update_song_label()
class SplashScreen(MDScreen):
    def on_enter(self):
        Clock.schedule_once(self.switch_to_lock, 3)

    def switch_to_lock(self, dt):
        self.manager.transition.direction = 'left'
        self.manager.current = 'lock'

if __name__ == "__main__":
    AniversarioApp().run()
