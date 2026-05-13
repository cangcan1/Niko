#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import os
from dotenv import load_dotenv
from niko_ai import NikoAI
from phone_features import PhoneFeatures
from voice_manager import VoiceManager
from todo_manager import TodoManager
from weather_dashboard import WeatherDashboard
import json
from datetime import datetime

load_dotenv()

class NikoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Niko - AI Tıbbi Asistan & Uydu Telefon")
        self.root.geometry("1100x800")
        self.root.configure(bg='#0a0e27')
        
        # Tema renkleri
        self.bg_color = '#0a0e27'
        self.accent_color = '#FF1493'  # Pembe
        self.text_color = '#FFFFFF'
        self.dark_bg = '#1a1f3a'
        
        # Modülleri yükle
        try:
            self.niko_ai = NikoAI(api_key=os.getenv('OPENAI_API_KEY'))
        except:
            self.niko_ai = None
            
        self.phone_features = PhoneFeatures()
        self.voice_manager = VoiceManager()
        self.todo_manager = TodoManager()
        self.weather_dashboard = WeatherDashboard()
        
        # Sesli dinleme durumu
        self.listening = False
        self.continuous_listening = True
        
        self.setup_ui()
        self.load_contacts()
        
        # Arka planda sesli dinlemeyi başlat
        self.start_continuous_listening()
        
    def setup_ui(self):
        """Ana arayüzü kuruyor"""
        # Üst panel - Niko Avatar
        top_frame = tk.Frame(self.root, bg=self.bg_color)
        top_frame.pack(fill=tk.X, pady=15)
        
        avatar_label = tk.Label(
            top_frame,
            text="●",
            font=("Arial", 60),
            fg=self.accent_color,
            bg=self.bg_color
        )
        avatar_label.pack(side=tk.LEFT, padx=20)
        self.avatar_label = avatar_label
        
        info_frame = tk.Frame(top_frame, bg=self.bg_color)
        info_frame.pack(side=tk.LEFT, padx=20, fill=tk.BOTH, expand=True)
        
        name_label = tk.Label(
            info_frame,
            text="NIKO - AI Tıbbi Asistan",
            font=("Arial", 16, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        )
        name_label.pack(anchor=tk.W)
        
        self.status_label = tk.Label(
            info_frame,
            text="🎤 Dinliyorum... 'Niko' deyin!",
            font=("Arial", 11),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.status_label.pack(anchor=tk.W)
        
        # Sekme paneli
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Stil ayarla
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.bg_color)
        style.configure('TNotebook.Tab', padding=[20, 10])
        style.map('TNotebook.Tab', background=[('selected', self.accent_color)])
        
        # 1. Chat Sekmesi
        self.chat_frame = tk.Frame(notebook, bg=self.dark_bg)
        notebook.add(self.chat_frame, text="💬 Chat")
        self.setup_chat_tab()
        
        # 2. Todo Sekmesi
        self.todo_frame = tk.Frame(notebook, bg=self.dark_bg)
        notebook.add(self.todo_frame, text="📝 Görevler")
        self.setup_todo_tab()
        
        # 3. Hava Durumu Sekmesi
        self.weather_frame = tk.Frame(notebook, bg=self.dark_bg)
        notebook.add(self.weather_frame, text="🌤️ Hava")
        self.setup_weather_tab()
        
        # 4. Ayarlar Sekmesi
        self.settings_frame = tk.Frame(notebook, bg=self.dark_bg)
        notebook.add(self.settings_frame, text="⚙️ Ayarlar")
        self.setup_settings_tab()
    
    def setup_chat_tab(self):
        """Chat sekmesini kuruyor"""
        # Chat ekranı
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame,
            height=20,
            width=100,
            bg=self.bg_color,
            fg=self.text_color,
            insertbackground=self.accent_color,
            font=("Courier", 10),
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat_display.config(state=tk.DISABLED)
        
        # Giriş paneli
        input_frame = tk.Frame(self.chat_frame, bg=self.dark_bg)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input_text = tk.Entry(
            input_frame,
            bg=self.bg_color,
            fg=self.text_color,
            insertbackground=self.accent_color,
            font=("Arial", 11)
        )
        self.input_text.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=5)
        self.input_text.bind('<Return>', lambda e: self.send_message())
        
        # Buton paneli
        button_frame = tk.Frame(self.chat_frame, bg=self.dark_bg)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        buttons = [
            ("🎤 Sesli", self.voice_input),
            ("📤 Gönder", self.send_message),
            ("📞 Ki şiler", self.show_contacts),
            ("🗑️ Temizle", self.clear_chat),
        ]
        
        for btn_text, cmd in buttons:
            btn = tk.Button(
                button_frame,
                text=btn_text,
                command=cmd,
                bg=self.accent_color,
                fg='#000000',
                font=("Arial", 10, "bold"),
                padx=15,
                pady=8
            )
            btn.pack(side=tk.LEFT, padx=5)
    
    def setup_todo_tab(self):
        """Todo sekmesini kuruyor"""
        input_frame = tk.Frame(self.todo_frame, bg=self.dark_bg)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            input_frame,
            text="Yeni Görev:",
            bg=self.dark_bg,
            fg=self.text_color,
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        
        self.todo_input = tk.Entry(
            input_frame,
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 10),
            width=50
        )
        self.todo_input.pack(side=tk.LEFT, expand=True, padx=5)
        self.todo_input.bind('<Return>', lambda e: self.add_todo())
        
        add_btn = tk.Button(
            input_frame,
            text="➕ Ekle",
            command=self.add_todo,
            bg=self.accent_color,
            fg='#000000',
            font=("Arial", 10, "bold")
        )
        add_btn.pack(side=tk.LEFT, padx=5)
        
        # Todo listesi
        list_frame = tk.Frame(self.todo_frame, bg=self.dark_bg)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.todo_listbox = tk.Listbox(
            list_frame,
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 11),
            yscrollcommand=scrollbar.set,
            selectmode=tk.SINGLE
        )
        self.todo_listbox.pack(fill=tk.BOTH, expand=True)
        self.todo_listbox.bind('<Double-Button-1>', lambda e: self.toggle_todo())
        scrollbar.config(command=self.todo_listbox.yview)
        
        # Buton paneli
        button_frame = tk.Frame(self.todo_frame, bg=self.dark_bg)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(
            button_frame,
            text="✅ Tamamla",
            command=self.toggle_todo,
            bg=self.accent_color,
            fg='#000000',
            font=("Arial", 10, "bold"),
            padx=15
        ).pack(side=tk.LEFT, padx=5)
        
        tk.Button(
            button_frame,
            text="🗑️ Sil",
            command=self.delete_todo,
            bg='#FF6B6B',
            fg='#FFFFFF',
            font=("Arial", 10, "bold"),
            padx=15
        ).pack(side=tk.LEFT, padx=5)
        
        self.refresh_todo_list()
    
    def setup_weather_tab(self):
        """Hava durumu sekmesini kuruyor"""
        search_frame = tk.Frame(self.weather_frame, bg=self.dark_bg)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Label(
            search_frame,
            text="Şehir:",
            bg=self.dark_bg,
            fg=self.text_color,
            font=("Arial", 10)
        ).pack(side=tk.LEFT, padx=5)
        
        self.weather_city_input = tk.Entry(
            search_frame,
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 10),
            width=30
        )
        self.weather_city_input.pack(side=tk.LEFT, padx=5, expand=True)
        self.weather_city_input.insert(0, "Istanbul")
        self.weather_city_input.bind('<Return>', lambda e: self.fetch_weather())
        
        tk.Button(
            search_frame,
            text="🔍 Ara",
            command=self.fetch_weather,
            bg=self.accent_color,
            fg='#000000',
            font=("Arial", 10, "bold")
        ).pack(side=tk.LEFT, padx=5)
        
        # Hava bilgisi gösterimi
        self.weather_display = scrolledtext.ScrolledText(
            self.weather_frame,
            height=20,
            width=100,
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 11),
            padx=10,
            pady=10
        )
        self.weather_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.weather_display.config(state=tk.DISABLED)
        
        # İlk yükleme
        self.fetch_weather()
    
    def setup_settings_tab(self):
        """Ayarlar sekmesini kuruyor"""
        settings_text = scrolledtext.ScrolledText(
            self.settings_frame,
            height=20,
            width=100,
            bg=self.bg_color,
            fg=self.text_color,
            font=("Courier", 10),
            padx=15,
            pady=15
        )
        settings_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        settings_text.config(state=tk.NORMAL)
        
        info = """🤖 NIKO - AI Tıbbi Asistan v1.0
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

📱 ÖZELLİKLER:

  💬 CHAT & KOMUTLAR
    • Sesli komut sistemi (tuşa basmadan)
    • Tıbbi belirti analizi (GPT-3 tabanlı)
    • T1bbi veritabanı (1000+ hastalık)
    • Chat geçmişi
  
  ☎️ TELEFON ÖZELLİKLERİ
    • Telefon çalma
    • SMS gönderme
    • Kişi yönetimi
    • Hatırlatıcılar
    • Timer & Alarm
  
  🎵 UYGULAMALAR
    • Müzik çalma
    • Web arama (DuckDuckGo)
    • Harita & Konum
    • Hava durumu
  
  📝 TODO LİSTESİ
    • Görev ekleme/silme
    • Tamamlama işareti
    • Otomatik kayıt
  
  🌤️ HAVA DURUMU
    • Gerçek zamanlı hava (OpenWeatherMap)
    • Sıcaklık, nem, rüzgar
    • Uyarılar

🎤 SESLI KOMUT KULLANIMI:

  1. Uygulamayı başlatın
  2. 'Niko' deyin
  3. Niko sesli cevap verecek
  4. Komutunuzu söyleyin
  5. Otomatik işlem yapılır

📝 ÖRNEK KOMUTLAR:

  • "Niko, başım ağrıyor"
  • "Niko, annemi ara"
  • "Niko, 5 dakika timer koy"
  • "Niko, yarın doktor randevum"
  • "Niko, hava durumu nasıl"

💾 DEPOLAMA:

  ✅ todos.json - Görev listesi
  ✅ reminders.json - Hatırlatıcılar
  ✅ contacts.json - Kişi listesi
  ✅ Chat geçmişi

⚙️ SISTEM GEREKSİNİMLERİ:

  ✓ Python 3.8+
  ✓ Mikrofon
  ✓ İnternet bağlantısı
  ✓ OpenAI API Anahtarı
  ✓ OpenWeatherMap API Anahtarı

📞 KİŞİLER:

  • Anne: +90555123456
  • Baba: +90555654321
  • Ali: +90555789012
  • Doktor: +90555345678
  • Ambulans: 112

🌐 API'LER:

  • OpenAI GPT-3 (Tıbbi analiz)
  • Google Speech Recognition (Ses tanıma)
  • DuckDuckGo (Web arama)
  • OpenWeatherMap (Hava durumu)

⚠️ DİKKAT:

  Niko t1bbi tavsiye değildir!
  Ciddi durumlarda her zaman doktora başvurun.

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🚀 Başlamak için Chat sekmesinde 'Niko' deyin!
"""
        
        settings_text.insert('1.0', info)
        settings_text.config(state=tk.DISABLED)
    
    def add_message(self, sender, text):
        """Chat'e mesaj ekleme"""
        self.chat_display.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: {text}\n\n")
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
        
        # Thread'de işleme
        threading.Thread(target=self.process_command, args=(message,), daemon=True).start()
    
    def process_command(self, text):
        """Komutu işleme"""
        text_lower = text.lower()
        
        try:
            if not self.niko_ai:
                self.add_message("Niko", "❌ OpenAI API anahtarı bulunamadı. .env dosyasını kontrol edin.")
                return
            
            # Telefon özellikleri
            if 'ara' in text_lower or 'telefon' in text_lower:
                contact_name = self.extract_contact(text)
                result = self.phone_features.make_call(contact_name)
                self.add_message("Niko", result)
                self.voice_manager.speak(result)
            
            elif 'mesaj' in text_lower or 'sms' in text_lower:
                contact_name = self.extract_contact(text)
                result = self.phone_features.send_sms(contact_name, text)
                self.add_message("Niko", result)
                self.voice_manager.speak(result)
            
            elif 'takvim' in text_lower or 'randevu' in text_lower or 'hatırla' in text_lower:
                result = self.phone_features.add_reminder(text)
                self.add_message("Niko", result)
                self.voice_manager.speak(result)
            
            elif 'timer' in text_lower or 'alarm' in text_lower:
                result = self.phone_features.set_timer(text)
                self.add_message("Niko", result)
                self.voice_manager.speak(result)
            
            elif 'müzik' in text_lower or 'şarkı' in text_lower:
                result = self.phone_features.play_music(text)
                self.add_message("Niko", result)
                self.voice_manager.speak(result)
            
            elif 'harita' in text_lower or 'yer' in text_lower or 'hastane' in text_lower:
                result = self.phone_features.find_location(text)
                self.add_message("Niko", result)
                self.voice_manager.speak(result)
            
            elif 'hava' in text_lower or 'hava durumu' in text_lower:
                result = self.phone_features.get_weather()
                self.add_message("Niko", result)
                self.voice_manager.speak(result)
            
            elif 'arama' in text_lower or 'araştır' in text_lower or 'internet' in text_lower:
                result = self.phone_features.web_search(text)
                self.add_message("Niko", result)
            
            else:
                # Tıbbi analiz
                response = self.niko_ai.analyze_symptoms(text)
                self.add_message("Niko", response)
                self.voice_manager.speak(response[:200])  # İlk 200 char sesli
        
        except Exception as e:
            error_msg = f"❌ Hata oluştu: {str(e)}"
            self.add_message("Niko", error_msg)
        
        self.status_label.config(text="🎤 Dinliyorum... 'Niko' deyin!")
    
    def voice_input(self):
        """Sesli giriş butonu"""
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
            self.add_message("Niko", f"❌ Ses tanıma hatası: {str(e)}")
        
        self.status_label.config(text="🎤 Dinliyorum... 'Niko' deyin!")
    
    def start_continuous_listening(self):
        """Arka planda sesli dinlemeyi başlat"""
        threading.Thread(target=self._continuous_listening_thread, daemon=True).start()
    
    def _continuous_listening_thread(self):
        """Arka planda sesli komut dinleme"""
        while self.continuous_listening:
            try:
                text = self.voice_manager.listen_without_timeout()
                
                if text and 'niko' in text.lower():
                    # Avatar animasyonu
                    self.avatar_label.config(fg='#FF69B4')
                    self.root.after(100, lambda: self.avatar_label.config(fg=self.accent_color))
                    
                    # Cevap ver
                    self.status_label.config(text="🎤 Dinliyorum (Detaylı)...")
                    self.voice_manager.speak("Buraday ım, ne yardimci olabilirim?")
                    
                    # Komutu dinle
                    command = self.voice_manager.listen()
                    if command and "hata" not in command.lower():
                        self.input_text.delete(0, tk.END)
                        self.input_text.insert(0, command)
                        self.root.after(100, self.send_message)
                    
                    self.status_label.config(text="🎤 Dinliyorum... 'Niko' deyin!")
                
            except Exception as e:
                continue
    
    def add_todo(self):
        """Görev ekleme"""
        text = self.todo_input.get().strip()
        if not text:
            messagebox.showwarning("Uyarı", "Görev metni giriniz!")
            return
        
        self.todo_manager.add_todo(text)
        self.todo_input.delete(0, tk.END)
        self.refresh_todo_list()
        self.add_message("Niko", f"✅ Görev eklendi: {text}")
    
    def toggle_todo(self):
        """Görev tamamlama durumunu değiştir"""
        selection = self.todo_listbox.curselection()
        if not selection:
            messagebox.showwarning("Uyarı", "Görev seçiniz!")
            return
        
        index = selection[0]
        self.todo_manager.toggle_todo(index)
        self.refresh_todo_list()
    
    def delete_todo(self):
        """Görev silme"""
        selection = self.todo_listbox.curselection()
        if not selection:
            messagebox.showwarning("Uyarı", "Görev seçiniz!")
            return
        
        index = selection[0]
        self.todo_manager.delete_todo(index)
        self.refresh_todo_list()
    
    def refresh_todo_list(self):
        """Todo listesini yenile"""
        self.todo_listbox.delete(0, tk.END)
        todos = self.todo_manager.get_todos()
        for todo in todos:
            status = "✅" if todo['completed'] else "⭕"
            self.todo_listbox.insert(tk.END, f"{status} {todo['text']}")
    
    def fetch_weather(self):
        """Hava durumunu getir"""
        city = self.weather_city_input.get().strip()
        if not city:
            city = "Istanbul"
        
        self.weather_display.config(state=tk.NORMAL)
        self.weather_display.delete(1.0, tk.END)
        self.weather_display.insert(tk.END, f"🔄 {city} için hava durumu yükleniyor...\n\n")
        self.weather_display.config(state=tk.DISABLED)
        
        threading.Thread(target=self._fetch_weather_thread, args=(city,), daemon=True).start()
    
    def _fetch_weather_thread(self, city):
        try:
            weather_info = self.weather_dashboard.get_weather(city)
            self.weather_display.config(state=tk.NORMAL)
            self.weather_display.delete(1.0, tk.END)
            self.weather_display.insert(tk.END, weather_info)
            self.weather_display.config(state=tk.DISABLED)
        except Exception as e:
            self.weather_display.config(state=tk.NORMAL)
            self.weather_display.delete(1.0, tk.END)
            self.weather_display.insert(tk.END, f"❌ Hata: {str(e)}")
            self.weather_display.config(state=tk.DISABLED)
    
    def show_contacts(self):
        """Kişileri göster"""
        try:
            with open('contacts.json', 'r', encoding='utf-8') as f:
                self.contacts = json.load(f)
        except:
            self.contacts = {}
        
        contacts_text = "📞 Kaydedilen Kişiler:\n\n"
        for name, phone in self.contacts.items():
            contacts_text += f"  • {name}: {phone}\n"
        
        self.add_message("Niko", contacts_text)
    
    def extract_contact(self, text):
        """Metinden kişi adı çıkart"""
        words = text.split()
        if len(words) > 1:
            return words[-1]
        return "Tanımsız"
    
    def clear_chat(self):
        """Chat temizle"""
        self.chat_display.config(state=tk.NORMAL)
        self.chat_display.delete(1.0, tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def load_contacts(self):
        """Kişileri yükle"""
        try:
            with open('contacts.json', 'r', encoding='utf-8') as f:
                self.contacts = json.load(f)
        except:
            self.contacts = {}

if __name__ == "__main__":
    root = tk.Tk()
    app = NikoApp(root)
    
    # Hoş geldiniz mesajı
    root.after(1000, lambda: app.add_message("Niko", "👋 Merhaba! Ben Niko, AI Tıbbi Asistan!\n\nBaşlamak için 'Niko' deyin ya da aşağıdaki butonları kullanın.\n\n🎤 Sesli komut, 📝 Görevler, 🌤️ Hava durumu ve daha fazlası!"))
    
    root.mainloop()
