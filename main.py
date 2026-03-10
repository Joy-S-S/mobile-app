from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
import requests
import re
import threading

# Configuration
TELEGRAM_BOT_TOKEN = "8442359669:AAEshVGNGINwuplxBLAhMis-DuVJcIBOazs"
TELEGRAM_API = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMyDescription"

class MamlkahMobile(App):
    def build(self):
        self.api_base = ""
        self.unreadd_count = 0
        self.alarm_playing = False
        try:
            self.sound = SoundLoader.load('assets/alarm_long.mp3')
        except:
            self.sound = None
        
        # Root Layout
        root = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(20))
        with root.canvas.before:
            Color(rgba=get_color_from_hex("#0f0c29"))
            self.rect = RoundedRectangle(pos=root.pos, size=root.size)
        root.bind(pos=self.update_rect, size=self.update_rect)

        # Header
        root.add_widget(Label(
            text="MAMLKAH MOBILE",
            font_size=dp(18),
            bold=True,
            color=get_color_from_hex("#00d2ff"),
            size_hint_y=None,
            height=dp(50)
        ))

        # Counter Section
        self.counter_label = Label(
            text="0",
            font_size=dp(80),
            bold=True,
            color=(1, 1, 1, 1)
        )
        root.add_widget(self.counter_label)
        root.add_widget(Label(
            text="UNREADD CHATS",
            font_size=dp(14),
            color=(0.7, 0.7, 0.7, 1),
            size_hint_y=None,
            height=dp(30)
        ))

        # Admin Alert Card (Simulated with Box)
        self.alert_box = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10), size_hint_y=None, height=dp(200), opacity=0)
        with self.alert_box.canvas.before:
            Color(rgba=(1, 1, 1, 0.05))
            self.alert_bg = RoundedRectangle(pos=self.alert_box.pos, size=self.alert_box.size, radius=[dp(20)])
        self.alert_box.bind(pos=self.update_alert_bg, size=self.update_alert_bg)

        self.alert_title = Label(text="ADMIN WAITING!", bold=True, color=get_color_from_hex("#e94560"))
        self.admin_info = Label(text="", font_size=dp(16))
        self.ack_btn = Button(
            text="ACKNOWLEDGE",
            background_color=(0, 0, 0, 0),
            size_hint_y=None,
            height=dp(50)
        )
        with self.ack_btn.canvas.before:
            Color(rgba=get_color_from_hex("#e94560"))
            self.btn_bg = RoundedRectangle(pos=self.ack_btn.pos, size=self.ack_btn.size, radius=[dp(10)])
        self.ack_btn.bind(pos=self.update_btn_bg, size=self.update_btn_bg)
        self.ack_btn.bind(on_release=self.handle_ack)

        self.alert_box.add_widget(self.alert_title)
        self.alert_box.add_widget(self.admin_info)
        self.alert_box.add_widget(self.ack_btn)
        root.add_widget(self.alert_box)

        # Start Polling
        Clock.schedule_interval(self.check_status, 5)
        
        return root

    def update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def update_alert_bg(self, instance, value):
        self.alert_bg.pos = instance.pos
        self.alert_bg.size = instance.size

    def update_btn_bg(self, instance, value):
        self.btn_bg.pos = instance.pos
        self.btn_bg.size = instance.size

    def check_status(self, dt):
        threading.Thread(target=self._fetch_thread).start()

    def _fetch_thread(self):
        try:
            if not self.api_base:
                resp = requests.get(TELEGRAM_API, timeout=5)
                desc = resp.json().get("result", {}).get("description", "")
                match = re.search(r"https://[a-z0-9-]+\.trycloudflare\.com", desc)
                if match:
                    self.api_base = f"{match[0]}/api/mobile"
                else:
                    return

            resp = requests.get(f"{self.api_base}/status", timeout=5)
            if resp.status_code == 200:
                data = resp.json()
                self.unreadd_count = data.get("unreadd_label_count", 0)
                alert = data.get("admin_alert", {})
                
                Clock.schedule_once(lambda dt: self.update_ui(alert))
        except:
            self.api_base = ""

    def update_ui(self, alert):
        self.counter_label.text = str(self.unreadd_count)
        if alert.get("active"):
            self.admin_info.text = f"{alert.get('name')}\n{alert.get('content')}"
            self.alert_box.opacity = 1
            if not self.alarm_playing and self.sound:
                self.sound.loop = True
                self.sound.play()
                self.alarm_playing = True
        else:
            self.alert_box.opacity = 0
            if self.alarm_playing and self.sound:
                self.sound.stop()
                self.alarm_playing = False

    def handle_ack(self, instance):
        threading.Thread(target=self._ack_thread).start()

    def _ack_thread(self):
        try:
            requests.post(f"{self.api_base}/ack", timeout=5)
        except:
            pass

if __name__ == "__main__":
    MamlkahMobile().run()
