#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import scrolledtext, messagebox, ttk
import threading
import os
from dotenv import load_dotenv
from niko_ai import NikoAI
from phone_features import PhoneFeatures
from voice_manager import VoiceManager
from todo_manager import TodoManager
from weather_dashboard import WeatherDashboard
import json

load_dotenv()

class NikoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🤖 Niko - AI Tıbbi Asistan")
        self.root.geometry("1100x800")
        self.root.configure(bg='#0a0e27')
        
        # Niko AI ve telefon özellikleri
        try:
            self.niko_ai = NikoAI(api_key=os.getenv('OPENAI_API_KEY'))
        except:
            self.niko_ai = NikoAI(api_key="demo")
        
        self.phone_features = PhoneFeatures()
        self.voice_manager = VoiceManager()
        self.todo_manager = TodoManager()
        self.weather_dashboard = WeatherDashboard()
        
        # Tema renkleri
        self.bg_color = '#0a0e27'
        self.accent_color = '#FF1493'  # Pembe
        self.text_color = '#FFFFFF'
        
        # Sesli dinleme durumu
        self.listening = False
        self.continuous_listening = True
        self.current_tab = 'chat'
        
        self.setup_ui()
        self.load_contacts()
        
        # Arka planda sürekli sesli komut dinlemesini başlat
        self.start_continuous_listening()
        
    def setup_ui(self):
        """Arayüzü kuruyor - Sekmeleri ve menüyü ekliyor"""
        # Üst panel - Başlık
        header_frame = tk.Frame(self.root, bg=self.accent_color, height=60)
        header_frame.pack(fill=tk.X)
        
        header_label = tk.Label(
            header_frame,
            text="🤖 NIKO - AI Tıbbi Asistan & Asistan",
            font=("Arial", 16, "bold"),
            fg='#000000',
            bg=self.accent_color
        )
        header_label.pack(pady=10)
        
        # Sekmeler (Tabs)
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # CSS stili ayarla
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.bg_color, borderwidth=0)
        style.configure('TNotebook.Tab', background=self.accent_color, foreground='#000000')
        style.map('TNotebook.Tab', background=[('selected', '#FF69B4')])
        
        # Sekme 1: Chat
        self.chat_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.chat_frame, text="💬 Chat")
        self.setup_chat_tab()
        
        # Sekme 2: Todo List
        self.todo_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.todo_frame, text="📝 Todo Liste")
        self.setup_todo_tab()
        
        # Sekme 3: Hava Durumu
        self.weather_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.weather_frame, text="🌤️ Hava Durumu")
        self.setup_weather_tab()
        
        # Sekme 4: Ayarlar
        self.settings_frame = tk.Frame(self.notebook, bg=self.bg_color)
        self.notebook.add(self.settings_frame, text="⚙️ Ayarlar")
        self.setup_settings_tab()
    
    def setup_chat_tab(self):
        """Chat sekmesini kuruyor"""
        # Avatar
        avatar_frame = tk.Frame(self.chat_frame, bg=self.bg_color)
        avatar_frame.pack(pady=10)
        
        avatar_label = tk.Label(
            avatar_frame,
            text="●",
            font=("Arial", 80),
            fg=self.accent_color,
            bg=self.bg_color
        )
        avatar_label.pack()
        self.avatar_label = avatar_label
        
        name_label = tk.Label(
            avatar_frame,
            text="NIKO",
            font=("Arial", 16, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        )
        name_label.pack()
        
        # Durum etiketi
        self.status_label = tk.Label(
            self.chat_frame,
            text="🎤 Dinliyorum... 'Niko' deyin!",
            font=("Arial", 11),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.status_label.pack()
        
        # Chat alanı
        chat_inner_frame = tk.Frame(self.chat_frame, bg=self.bg_color)
        chat_inner_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_inner_frame,
            height=20,
            width=100,
            bg='#1a1f3a',
            fg=self.text_color,
            insertbackground=self.accent_color,
            font=("Arial", 10)
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Giriş alanı
        input_frame = tk.Frame(self.chat_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.input_text = tk.Entry(
            input_frame,
            bg='#1a1f3a',
            fg=self.text_color,
            insertbackground=self.accent_color,
            font=("Arial", 11)
        )
        self.input_text.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=5)
        self.input_text.bind('<Return>', lambda e: self.send_message())
        
        # Buton paneli
        button_frame = tk.Frame(self.chat_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=15, pady=10)
        
        buttons = [
            ("🎤 Sesli", self.voice_input),
            ("📤 Gönder", self.send_message),
            ("📞 Kişiler", self.show_contacts),
            ("🌍 Arama", self.web_search),
            ("🎵 Müzik", self.play_music),
            ("📍 Harita", self.show_map),
        ]
        
        for btn_text, cmd in buttons:
            btn = tk.Button(
                button_frame,
                text=btn_text,
                command=cmd,
                bg=self.accent_color,
                fg='#000000',
                font=("Arial", 9, "bold"),
                padx=10,
                pady=5
            )
            btn.pack(side=tk.LEFT, padx=3)
    
    def setup_todo_tab(self):
        """Todo List sekmesini kuruyor"""
        # Başlık
        title_label = tk.Label(
            self.todo_frame,
            text="📝 Görev Listesi",
            font=("Arial", 14, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        title_label.pack(pady=10)
        
        # Giriş alanı
        input_frame = tk.Frame(self.todo_frame, bg=self.bg_color)
        input_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.todo_input = tk.Entry(
            input_frame,
            bg='#1a1f3a',
            fg=self.text_color,
            insertbackground=self.accent_color,
            font=("Arial", 11)
        )
        self.todo_input.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=5)
        self.todo_input.bind('<Return>', lambda e: self.add_todo())
        
        add_btn = tk.Button(
            input_frame,
            text="➕ Ekle",
            command=self.add_todo,
            bg=self.accent_color,
            fg='#000000',
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Todo listesi
        list_frame = tk.Frame(self.todo_frame, bg=self.bg_color)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        
        self.todo_display = tk.Listbox(
            list_frame,
            bg='#1a1f3a',
            fg=self.text_color,
            font=("Arial", 11),
            borderwidth=0,
            activestyle='none'
        )
        self.todo_display.pack(fill=tk.BOTH, expand=True)
        self.todo_display.bind('<Double-Button-1>', self.toggle_todo)
        
        # Butonlar
        button_frame = tk.Frame(self.todo_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=15, pady=10)
        
        tk.Button(
            button_frame,
            text="🗑️ Sil",
            command=self.delete_todo,
            bg='#FF6B6B',
            fg='#FFFFFF',
            font=("Arial", 10, "bold"),
            padx=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="🔄 Yenile",
            command=self.refresh_todo_list,
            bg=self.accent_color,
            fg='#000000',
            font=("Arial", 10, "bold"),
            padx=10
        ).pack(side=tk.LEFT, padx=5)
        
        self.refresh_todo_list()
    
    def setup_weather_tab(self):
        """Hava Durumu sekmesini kuruyor"""
        # Başlık
        title_label = tk.Label(
            self.weather_frame,
            text="🌤️ Hava Durumu Gösterge Paneli",
            font=("Arial", 14, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        title_label.pack(pady=10)
        
        # Şehir arama
        search_frame = tk.Frame(self.weather_frame, bg=self.bg_color)
        search_frame.pack(fill=tk.X, padx=15, pady=10)
        
        self.weather_input = tk.Entry(
            search_frame,
            bg='#1a1f3a',
            fg=self.text_color,
            insertbackground=self.accent_color,
            font=("Arial", 11)
        )
        self.weather_input.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=5)
        self.weather_input.insert(0, "İstanbul")
        self.weather_input.bind('<Return>', lambda e: self.fetch_weather())
        
        search_btn = tk.Button(
            search_frame,
            text="🔍 Ara",
            command=self.fetch_weather,
            bg=self.accent_color,
            fg='#000000',
            font=("Arial", 10, "bold"),
            padx=15
        )
        search_btn.pack(side=tk.LEFT, padx=5)
        
        # Hava durumu bilgisi
        self.weather_display = scrolledtext.ScrolledText(
            self.weather_frame,
            height=25,
            width=100,
            bg='#1a1f3a',
            fg=self.text_color,
            font=("Arial", 11),
            borderwidth=0
        )
        self.weather_display.pack(fill=tk.BOTH, expand=True, padx=15, pady=10)
        self.weather_display.config(state=tk.DISABLED)
        
        # İlk yükleme
        self.fetch_weather()
    
    def setup_settings_tab(self):
        """Ayarlar sekmesini kuruyor"""
        # Başlık
        title_label = tk.Label(
            self.settings_frame,
            text="⚙️ Niko Ayarları",
            font=("Arial", 14, "bold"),
            fg=self.accent_color,
            bg=self.bg_color
        )
        title_label.pack(pady=20)
        
        # Bilgiler
        info_text = """🤖 NIKO - AI Tıbbi Asistan v1.0

📋 Özellikler:
  ✓ Yapay Zeka tabanlı tıbbi tavsiye
  ✓ Sesli komut (Türkçe)
  ✓ Telefon özellikleri
  ✓ Todo List yönetimi
  ✓ Hava Durumu gösterge paneli
  ✓ Web arama
  ✓ Harita ve konum
  ✓ Müzik çalma

🎯 Nasıl Kullanılır:
  1. Chat sekmesinde 'Niko' deyin
  2. Belirtilerinizi söyleyin veya yazın
  3. Niko sesli ve yazılı cevap verir
  4. Todo List'te görev yönetin
  5. Hava durumunu takip edin

⚠️ ÖNEMLİ:
  • Niko tıbbi tavsiye değildir
  • Ciddi durumlarda doktora başvurun
  • Kişisel bilgileriniz gizlidir
  • API anahtarınızı gizli tutun

💻 Sistem Gereksinimleri:
  • Python 3.8+
  • Mikrofon
  • İnternet bağlantısı
  • OpenAI API Anahtarı

📞 Destek: github.com/cangcan1/Niko
        """
        
        info_label = tk.Label(
            self.settings_frame,
            text=info_text,
            font=("Arial", 11),
            fg=self.text_color,
            bg=self.bg_color,
            justify=tk.LEFT
        )
        info_label.pack(pady=20, padx=30)
        
        # Butonlar
        button_frame = tk.Frame(self.settings_frame, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=15, pady=20)
        
        tk.Button(
            button_frame,
            text="✅ Hakkında",
            command=lambda: messagebox.showinfo(
                "Niko Hakkında",
                "🤖 NIKO - AI Tıbbi Asistan\n\nSürüm: 1.0\nGeliştiriciler: cangcan1\n\nNiko, modern yapay zeka teknolojisi kullanarak tıbbi tavsiye ve asistan hizmetleri sunar."
            ),
            bg=self.accent_color,
            fg='#000000',
            font=("Arial", 10, "bold"),
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="🔄 Ayarları Sıfırla",
            command=lambda: messagebox.showinfo(
                "Sıfırla",
                "Ayarlar sıfırlandı!\nUygulamayı yeniden başlatın."
            ),
            bg='#FFA500',
            fg='#000000',
            font=("Arial", 10, "bold"),
            padx=20,
            pady=10
        ).pack(side=tk.LEFT, padx=5)
    
    def add_message(self, sender, text):
        """Chat'e mesaj ekleme"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.insert(tk.END, f"\n{sender}: {text}\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def send_message(self):
        """Mesaj gönderme ve işleme"""
        message = self.input_text.get().strip()
        if not message:
            return
        
        self.input_text.delete(0, tk.END)
        self.add_message("Siz", message)
        self.status_label.config(text="🤔 Düşünüyorum...")
        
        threading.Thread(target=self.process_command, args=(message,), daemon=True).start()
    
    def process_command(self, text):
        """Komutu işleme ve uygun özelliği çalıştırma"""
        text_lower = text.lower()
        
        try:
            # Telefon özellikleri kontrol etme
            if 'ara' in text_lower or 'telefon' in text_lower:
                self.handle_call(text)
            elif 'mesaj' in text_lower or 'sms' in text_lower:
                self.handle_sms(text)
            elif 'takvim' in text_lower or 'randevu' in text_lower or 'hatırla' in text_lower:
                self.handle_calendar(text)
            elif 'timer' in text_lower or 'alarm' in text_lower:
                self.handle_timer(text)
            elif 'müzik' in text_lower or 'şarkı' in text_lower:
                self.handle_music(text)
            elif 'harita' in text_lower or 'yer' in text_lower or 'hastane' in text_lower:
                self.handle_map(text)
            elif 'hava' in text_lower or 'hava durumu' in text_lower:
                self.handle_weather_command(text)
            elif 'arama' in text_lower or 'araştır' in text_lower or 'internet' in text_lower:
                self.handle_web_search(text)
            else:
                # Tıbbi analiz
                response = self.niko_ai.analyze_symptoms(text)
                self.add_message("Niko", response)
                try:
                    self.voice_manager.speak(response[:150])
                except:
                    pass
        
        except Exception as e:
            error_msg = f"Hata oluştu: {str(e)}"
            self.add_message("Niko", error_msg)
        
        self.status_label.config(text="🎤 Dinliyorum... 'Niko' deyin!")
    
    def handle_call(self, text):
        """Telefon çalması"""
        contact_name = self.extract_contact(text)
        result = self.phone_features.make_call(contact_name)
        self.add_message("Niko", result)
        try:
            self.voice_manager.speak(result)
        except:
            pass
    
    def handle_sms(self, text):
        """Mesaj gönderme"""
        contact_name = self.extract_contact(text)
        result = self.phone_features.send_sms(contact_name, text)
        self.add_message("Niko", result)
        try:
            self.voice_manager.speak(result)
        except:
            pass
    
    def handle_calendar(self, text):
        """Takvim ve hatırlatıcı"""
        result = self.phone_features.add_reminder(text)
        self.add_message("Niko", result)
        try:
            self.voice_manager.speak(result)
        except:
            pass
    
    def handle_timer(self, text):
        """Timer ve alarm"""
        result = self.phone_features.set_timer(text)
        self.add_message("Niko", result)
        try:
            self.voice_manager.speak(result)
        except:
            pass
    
    def handle_music(self, text):
        """Müzik çalma"""
        result = self.phone_features.play_music(text)
        self.add_message("Niko", result)
        try:
            self.voice_manager.speak(result)
        except:
            pass
    
    def handle_map(self, text):
        """Harita ve konum"""
        result = self.phone_features.find_location(text)
        self.add_message("Niko", result)
        try:
            self.voice_manager.speak(result)
        except:
            pass
    
    def handle_weather_command(self, text):
        """Hava durumu komutu"""
        result = "🌤️ Hava Durumu sekmesini açıyorum..."
        self.add_message("Niko", result)
        self.notebook.select(2)  # Hava Durumu sekmesine git
    
    def handle_web_search(self, text):
        """İnternet arama"""
        result = self.phone_features.web_search(text)
        self.add_message("Niko", result)
        try:
            self.voice_manager.speak(result[:100])
        except:
            pass
    
    def extract_contact(self, text):
        """Metinden kişi adı çıkarma"""
        words = text.split()
        if len(words) > 1:
            return words[-1]
        return "Tanımsız"
    
    def voice_input(self):
        """Sesli giriş"""
        self.status_label.config(text="🎤 Dinliyorum...")
        threading.Thread(target=self._voice_input_thread, daemon=True).start()
    
    def _voice_input_thread(self):
        try:
            text = self.voice_manager.listen()
            if text and "hata" not in text.lower():
                self.input_text.delete(0, tk.END)
                self.input_text.insert(0, text)
                self.root.after(100, self.send_message)
        except Exception as e:
            self.add_message("Niko", f"Ses tanıma hatası: {str(e)}")
        
        self.status_label.config(text="🎤 Dinliyorum... 'Niko' deyin!")
    
    def start_continuous_listening(self):
        """Arka planda sürekli sesli komut dinlemesini başlat"""
        threading.Thread(target=self._continuous_listening_thread, daemon=True).start()
    
    def _continuous_listening_thread(self):
        """Arka planda sürekli dinleme yapan thread"""
        import time
        while self.continuous_listening:
            try:
                text = self.voice_manager.listen_without_timeout()
                
                if text and 'niko' in text.lower():
                    # Avatar renk değişimi (canlanma)
                    self.avatar_label.config(fg='#FF69B4')
                    self.root.after(100, lambda: self.avatar_label.config(fg=self.accent_color))
                    
                    self.status_label.config(text="💬 Evet, buradayım! Ne istiyorsunuz?")
                    try:
                        self.voice_manager.speak("Buraday ım, ne yardimci olabilirim?")
                    except:
                        pass
                    
                    # Komut dinle
                    time.sleep(0.5)
                    command = self.voice_manager.listen()
                    if command and command != "Anlamadım, lütfen tekrar söyleyin." and "hata" not in command.lower():
                        self.input_text.delete(0, tk.END)
                        self.input_text.insert(0, command)
                        self.root.after(100, self.send_message)
                    
                    self.status_label.config(text="🎤 Dinliyorum... 'Niko' deyin!")
                
            except Exception as e:
                continue
            
            time.sleep(0.1)
    
    def show_contacts(self):
        """Kişiler listesi gösterme"""
        contacts_text = "📞 Kaydedilen Kişiler:\n\n"
        for name, phone in self.contacts.items():
            contacts_text += f"  • {name}: {phone}\n"
        self.add_message("Niko", contacts_text)
    
    def web_search(self):
        """Web arama başlatma"""
        self.input_text.insert(0, "Bunu araştır: ")
    
    def play_music(self):
        """Müzik çalma"""
        self.input_text.insert(0, "Müzik çal: ")
    
    def show_map(self):
        """Harita gösterme"""
        self.input_text.insert(0, "Yakındaki harita göster: ")
    
    def add_todo(self):
        """Todo ekleme"""
        task = self.todo_input.get().strip()
        if task:
            self.todo_manager.add_task(task)
            self.todo_input.delete(0, tk.END)
            self.refresh_todo_list()
    
    def toggle_todo(self, event):
        """Todo tamamla/tamamlanmadı işaretle"""
        selection = self.todo_display.curselection()
        if selection:
            idx = selection[0]
            self.todo_manager.toggle_task(idx)
            self.refresh_todo_list()
    
    def delete_todo(self):
        """Todo silme"""
        selection = self.todo_display.curselection()
        if selection:
            idx = selection[0]
            self.todo_manager.delete_task(idx)
            self.refresh_todo_list()
    
    def refresh_todo_list(self):
        """Todo listesini yenile"""
        self.todo_display.delete(0, tk.END)
        tasks = self.todo_manager.get_tasks()
        for idx, task in enumerate(tasks):
            status = "✅" if task['completed'] else "⭕"
            self.todo_display.insert(tk.END, f"{status} {task['title']}")
    
    def fetch_weather(self):
        """Hava durumunu getir"""
        city = self.weather_input.get().strip() or "İstanbul"
        weather_info = self.weather_dashboard.get_weather(city)
        
        self.weather_display.config(state=tk.NORMAL)
        self.weather_display.delete('1.0', tk.END)
        self.weather_display.insert(tk.END, weather_info)
        self.weather_display.config(state=tk.DISABLED)
    
    def load_contacts(self):
        """Kişileri yükleme"""
        try:
            with open('contacts.json', 'r', encoding='utf-8') as f:
                self.contacts = json.load(f)
        except:
            self.contacts = {}

if __name__ == "__main__":
    root = tk.Tk()
    app = NikoApp(root)
    root.mainloop()
