#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
import threading
import os
from dotenv import load_dotenv

# İsteğe bağlı imports
try:
    from niko_ai import NikoAI
except:
    NikoAI = None

try:
    from phone_features import PhoneFeatures
except:
    PhoneFeatures = None

try:
    from voice_manager import VoiceManager
except:
    VoiceManager = None

try:
    from todo_manager import TodoManager
except:
    TodoManager = None

try:
    from weather_dashboard import WeatherDashboard
except:
    WeatherDashboard = None

import json
from datetime import datetime

load_dotenv()

class NikoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Niko - AI Tıbbi Asistan")
        self.root.geometry("1000x700")
        self.root.configure(bg='#0a0e27')
        
        # Tema
        self.bg_color = '#0a0e27'
        self.accent_color = '#FF1493'
        self.text_color = '#FFFFFF'
        self.dark_bg = '#1a1f3a'
        
        # Modüller
        self.niko_ai = NikoAI(api_key=os.getenv('OPENAI_API_KEY')) if NikoAI else None
        self.phone_features = PhoneFeatures() if PhoneFeatures else None
        self.voice_manager = VoiceManager() if VoiceManager else None
        self.todo_manager = TodoManager() if TodoManager else None
        self.weather_dashboard = WeatherDashboard() if WeatherDashboard else None
        
        self.continuous_listening = True
        self.setup_ui()
        self.load_contacts()
        self.start_continuous_listening()
        
    def setup_ui(self):
        """Arayüzü kur"""
        # Üst panel
        top_frame = tk.Frame(self.root, bg=self.bg_color)
        top_frame.pack(fill=tk.X, pady=15)
        
        avatar_label = tk.Label(
            top_frame,
            text="●",
            font=("Arial", 50),
            fg=self.accent_color,
            bg=self.bg_color
        )
        avatar_label.pack(side=tk.LEFT, padx=20)
        self.avatar_label = avatar_label
        
        info_frame = tk.Frame(top_frame, bg=self.bg_color)
        info_frame.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)
        
        tk.Label(
            info_frame,
            text="NIKO",
            font=("Arial", 16, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        ).pack(anchor=tk.W)
        
        self.status_label = tk.Label(
            info_frame,
            text="🎤 Dinliyorum... 'Niko' deyin!",
            font=("Arial", 10),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.status_label.pack(anchor=tk.W)
        
        # Notebook (Sekmeler)
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Stil
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background=self.bg_color)
        style.configure('TNotebook.Tab', padding=[15, 8])
        
        # Sekmeler
        self.chat_frame = tk.Frame(notebook, bg=self.dark_bg)
        notebook.add(self.chat_frame, text="💬 Chat")
        self.setup_chat_tab()
        
        self.todo_frame = tk.Frame(notebook, bg=self.dark_bg)
        notebook.add(self.todo_frame, text="📝 Görevler")
        self.setup_todo_tab()
        
        self.weather_frame = tk.Frame(notebook, bg=self.dark_bg)
        notebook.add(self.weather_frame, text="🌤️ Hava")
        self.setup_weather_tab()
        
        self.settings_frame = tk.Frame(notebook, bg=self.dark_bg)
        notebook.add(self.settings_frame, text="⚙️ Ayarlar")
        self.setup_settings_tab()
    
    def setup_chat_tab(self):
        """Chat sekmesi"""
        self.chat_display = scrolledtext.ScrolledText(
            self.chat_frame,
            bg=self.bg_color,
            fg=self.text_color,
            font=("Courier", 10),
            padx=10,
            pady=10
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.chat_display.config(state=tk.DISABLED)
        
        input_frame = tk.Frame(self.chat_frame, bg=self.dark_bg)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.input_text = tk.Entry(
            input_frame,
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 11)
        )
        self.input_text.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=5)
        self.input_text.bind('<Return>', lambda e: self.send_message())
        
        button_frame = tk.Frame(self.chat_frame, bg=self.dark_bg)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(button_frame, text="🎤 Sesli", command=self.voice_input, bg=self.accent_color, fg='#000').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="📤 Gönder", command=self.send_message, bg=self.accent_color, fg='#000').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🗑️ Temizle", command=self.clear_chat, bg=self.accent_color, fg='#000').pack(side=tk.LEFT, padx=5)
    
    def setup_todo_tab(self):
        """Todo sekmesi"""
        input_frame = tk.Frame(self.todo_frame, bg=self.dark_bg)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.todo_input = tk.Entry(
            input_frame,
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 10)
        )
        self.todo_input.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=5)
        self.todo_input.bind('<Return>', lambda e: self.add_todo())
        
        tk.Button(input_frame, text="➕ Ekle", command=self.add_todo, bg=self.accent_color, fg='#000').pack(side=tk.LEFT, padx=5)
        
        list_frame = tk.Frame(self.todo_frame, bg=self.dark_bg)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.todo_listbox = tk.Listbox(
            list_frame,
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 11)
        )
        self.todo_listbox.pack(fill=tk.BOTH, expand=True)
        self.todo_listbox.bind('<Double-Button-1>', lambda e: self.toggle_todo())
        
        button_frame = tk.Frame(self.todo_frame, bg=self.dark_bg)
        button_frame.pack(fill=tk.X, padx=10, pady=10)
        
        tk.Button(button_frame, text="✅ Tamamla", command=self.toggle_todo, bg=self.accent_color, fg='#000').pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="🗑️ Sil", command=self.delete_todo, bg='#FF6B6B', fg='#FFF').pack(side=tk.LEFT, padx=5)
        
        self.refresh_todo_list()
    
    def setup_weather_tab(self):
        """Hava durumu sekmesi"""
        search_frame = tk.Frame(self.weather_frame, bg=self.dark_bg)
        search_frame.pack(fill=tk.X, padx=10, pady=10)
        
        self.weather_city_input = tk.Entry(
            search_frame,
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 10)
        )
        self.weather_city_input.pack(fill=tk.X, side=tk.LEFT, expand=True, padx=5)
        self.weather_city_input.insert(0, "Istanbul")
        self.weather_city_input.bind('<Return>', lambda e: self.fetch_weather())
        
        tk.Button(search_frame, text="🔍 Ara", command=self.fetch_weather, bg=self.accent_color, fg='#000').pack(side=tk.LEFT, padx=5)
        
        self.weather_display = scrolledtext.ScrolledText(
            self.weather_frame,
            bg=self.bg_color,
            fg=self.text_color,
            font=("Arial", 10),
            padx=10,
            pady=10
        )
        self.weather_display.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        self.weather_display.config(state=tk.DISABLED)
        
        self.fetch_weather()
    
    def setup_settings_tab(self):
        """Ayarlar sekmesi"""
        settings_text = scrolledtext.ScrolledText(
            self.settings_frame,
            bg=self.bg_color,
            fg=self.text_color,
            font=("Courier", 9),
            padx=15,
            pady=15
        )
        settings_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        settings_text.config(state=tk.NORMAL)
        
        info = """🤖 NIKO - AI Tıbbi Asistan v1.0
═══════════════════════════════════════════════════

📱 ÖZELLİKLER:

💬 CHAT & KOMUTLAR
  • Sesli komut sistemi
  • Tıbbi belirti analizi
  • Chat geçmişi

☎️ TELEFON ÖZELLİKLERİ
  • Telefon çalma
  • SMS gönderme
  • Kişi yönetimi
  • Hatırlatıcılar

🎵 UYGULAMALAR
  • Müzik çalma
  • Web arama
  • Harita & Konum
  • Hava durumu

📝 TODO LİSTESİ
  • Görev ekleme/silme
  • Tamamlama işareti
  • Otomatik kayıt

🌤️ HAVA DURUMU
  • Gerçek zamanlı hava
  • Sıcaklık, nem, rüzgar
  • Günlük tahmin

🎤 SESLI KOMUT KULLANIMI:

1. 'Niko' deyin
2. Niko sesli cevap verecek
3. Komutunuzu söyleyin
4. Otomatik işlem yapılır

📋 ÖRNEK KOMUTLAR:

  • "Niko, başım ağrıyor"
  • "Niko, annemi ara"
  • "Niko, 5 dakika timer"
  • "Niko, yarın doktor randevum"
  • "Niko, hava durumu"

💾 DEPOLAMA:

  ✓ todos.json - Görevler
  ✓ reminders.json - Hatırlatıcılar
  ✓ contacts.json - Kişiler

⚙️ SISTEM GEREKSİNİMLERİ:

  ✓ Python 3.8+
  ✓ Mikrofon
  ✓ İnternet bağlantısı
  ✓ OpenAI API Anahtarı (.env)

═══════════════════════════════════════════════════

🚀 BAŞLAMAK İÇİN:

1. pip install -r requirements.txt
2. .env dosyasına OpenAI API anahtarı ekleyin
3. NIKO BAŞLADIIIII!

⚠️ DİKKAT:

Niko tıbbi tavsiye DEĞİLDİR!
Ciddi durumlarda doktora başvurun.
═══════════════════════════════════════════════════"""
        
        settings_text.insert('1.0', info)
        settings_text.config(state=tk.DISABLED)
    
    def add_message(self, sender, text):
        """Mesaj ekle"""
        self.chat_display.config(state=tk.NORMAL)
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.chat_display.insert(tk.END, f"[{timestamp}] {sender}: {text}\n\n")
        self.chat_display.see(tk.END)
        self.chat_display.config(state=tk.DISABLED)
    
    def send_message(self):
        """Mesaj gönder"""
        message = self.input_text.get().strip()
        if not message:
            return
        
        self.input_text.delete(0, tk.END)
        self.add_message("Siz", message)
        self.status_label.config(text="🤔 Düşünüyorum...")
        
        threading.Thread(target=self.process_command, args=(message,), daemon=True).start()
    
    def process_command(self, text):
        """Komutu işle"""
        try:
            if not self.niko_ai:
                self.add_message("Niko", "❌ OpenAI API anahtarı bulunamadı. .env dosyasını kontrol edin.")
            else:
                response = self.niko_ai.analyze_symptoms(text)
                self.add_message("Niko", response)
                
                if self.voice_manager:
                    try:
                        self.voice_manager.speak(response[:150])
                    except:
                        pass
        except Exception as e:
            self.add_message("Niko", f"❌ Hata: {str(e)}")
        
        self.status_label.config(text="🎤 Dinliyorum... 'Niko' deyin!")
    
    def voice_input(self):
        """Sesli giriş"""
        if not self.voice_manager:
            messagebox.showerror("Hata", "Ses sistemi yüklenmedi!")
            return
        
        self.status_label.config(text="🎤 Dinliyorum...")
        threading.Thread(target=self._voice_input_thread, daemon=True).start()
    
    def _voice_input_thread(self):
        try:
            text = self.voice_manager.listen()
            if text and "hata" not in text.lower():
                self.input_text.delete(0, tk.END)
                self.input_text.insert(0, text)
                self.root.after(100, self.send_message)
        except:
            pass
        
        self.status_label.config(text="🎤 Dinliyorum... 'Niko' deyin!")
    
    def start_continuous_listening(self):
        """Arka planda sesli dinleme"""
        if self.voice_manager:
            threading.Thread(target=self._continuous_listening_thread, daemon=True).start()
    
    def _continuous_listening_thread(self):
        """Arka planda dinleme"""
        while self.continuous_listening:
            try:
                text = self.voice_manager.listen_without_timeout()
                if text and 'niko' in text.lower():
                    self.avatar_label.config(fg='#FF69B4')
                    self.root.after(100, lambda: self.avatar_label.config(fg=self.accent_color))
                    self.status_label.config(text="👂 Dinliyorum (Detaylı)...")
                    
                    self.voice_manager.speak("Buraday ım, ne yardimci olabilirim?")
                    command = self.voice_manager.listen()
                    
                    if command and "hata" not in command.lower():
                        self.input_text.delete(0, tk.END)
                        self.input_text.insert(0, command)
                        self.root.after(100, self.send_message)
                    
                    self.status_label.config(text="🎤 Dinliyorum... 'Niko' deyin!")
            except:
                continue
    
    def add_todo(self):
        """Görev ekle"""
        text = self.todo_input.get().strip()
        if not text:
            messagebox.showwarning("Uyarı", "Görev metni giriniz!")
            return
        
        if self.todo_manager:
            self.todo_manager.add_todo(text)
            self.todo_input.delete(0, tk.END)
            self.refresh_todo_list()
    
    def toggle_todo(self):
        """Görev tamamla"""
        selection = self.todo_listbox.curselection()
        if not selection or not self.todo_manager:
            return
        
        self.todo_manager.toggle_todo(selection[0])
        self.refresh_todo_list()
    
    def delete_todo(self):
        """Görev sil"""
        selection = self.todo_listbox.curselection()
        if not selection or not self.todo_manager:
            return
        
        self.todo_manager.delete_todo(selection[0])
        self.refresh_todo_list()
    
    def refresh_todo_list(self):
        """Todo listesi güncelle"""
        self.todo_listbox.delete(0, tk.END)
        if self.todo_manager:
            todos = self.todo_manager.get_todos()
            for todo in todos:
                status = "✅" if todo['completed'] else "⭕"
                self.todo_listbox.insert(tk.END, f"{status} {todo['text']}")
    
    def fetch_weather(self):
        """Hava durumunu getir"""
        if not self.weather_dashboard:
            self.weather_display.config(state=tk.NORMAL)
            self.weather_display.delete(1.0, tk.END)
            self.weather_display.insert(tk.END, "❌ Hava durumu sistemi yüklenmedi!")
            self.weather_display.config(state=tk.DISABLED)
            return
        
        city = self.weather_city_input.get().strip() or "Istanbul"
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
    
    def clear_chat(self):
        """Chati temizle"""
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
    root.after(1000, lambda: app.add_message("Niko", "👋 Merhaba! Ben Niko, AI Tıbbi Asistan!\n\nBaşlamak için 'Niko' deyin veya butonları kullanın."))
    root.mainloop()
