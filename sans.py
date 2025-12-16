from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Rectangle, Line
from kivy.core.window import Window
from kivy.clock import Clock
import os

YOL = os.path.dirname(os.path.abspath(__file__))

class SansBattle(Widget):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.hp = 92
        self.karma = 0
        self.box_size = 500
        self.box_x = (Window.width - self.box_size) / 2
        self.box_y = 350 
        
        self.heart_pos = [Window.width/2, self.box_y + 100]
        
        # Resim yolları
        self.sans_path = os.path.join(YOL, 'sans.jpg')
        self.gb_path = os.path.join(YOL, 'gb.jpg')

        Clock.schedule_interval(self.update, 1.0/60.0)

    def update(self, dt):
        self.canvas.clear()
        with self.canvas:
            # Tüm ekran siyah
            Color(0, 0, 0, 1)
            Rectangle(size=Window.size)
            
            # --- SANS GÖRSELİ ---
            # Beyaz arka planı olan bir JPG kullandığın için Color'ı tam beyaz yapıyoruz
            Color(1, 1, 1, 1)
            # Sans'ın etrafındaki beyazlık sırıtabilir, o yüzden siyah ekranda 
            # düzgün dursun diye boyutunu ayarlıyoruz.
            Rectangle(source=self.sans_path, 
                      pos=(Window.width/2 - 125, Window.height - 350), 
                      size=(250, 280))
            
            # --- SAVAŞ KUTUSU ---
            Color(1, 1, 1, 1)
            Line(rectangle=(self.box_x, self.box_y, self.box_size, self.box_size), width=5)

            # --- HP & KR BARI (Kutunun üstünde) ---
            # Kırmızı zemin (Eriyen can)
            Color(1, 0, 0, 1)
            Rectangle(pos=(self.box_x, self.box_y + self.box_size + 20), size=(300, 25))
            # Sarı can (Mevcut can)
            Color(1, 1, 0, 1)
            Rectangle(pos=(self.box_x, self.box_y + self.box_size + 20), size=(max(0, self.hp * 3.2), 25))
            # Mor KR (Karma - Sarı canın bittiği yerden başlar)
            Color(1, 0, 1, 1)
            Rectangle(pos=(self.box_x + self.hp * 3.2, self.box_y + self.box_size + 20), size=(self.karma * 3.2, 25))

            # --- KALP (RUH) ---
            Color(1, 0, 0, 1)
            Rectangle(pos=self.heart_pos, size=(30, 30))

        # Karma etkisiyle canın azalması
        if self.karma > 0:
            self.hp -= 0.05
            self.karma -= 0.05
        
        if self.hp <= 0: App.get_running_app().stop()

    def on_touch_move(self, touch):
        # Kalbi kutunun içinde tut
        self.heart_pos[0] = max(self.box_x + 5, min(touch.x - 15, self.box_x + self.box_size - 35))
        self.heart_pos[1] = max(self.box_y + 5, min(touch.y - 15, self.box_y + self.box_size - 35))

class SansApp(App):
    def build(self): return SansBattle()

SansApp().run()
