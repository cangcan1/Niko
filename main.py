#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import tkinter as tk
from tkinter import scrolledtext, messagebox
import threading
import os
from dotenv import load_dotenv
from niko_ai import NikoAI
from phone_features import PhoneFeatures
from voice_manager import VoiceManager
import json

load_dotenv()

class NikoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Niko - AI Tıbbi Asistan")
        self.root.geometry("900x700")
        self.root.configure(bg='#0a0e27')
        
        # Niko AI ve telefon özellikleri
        self.niko_ai = NikoAI(api_key=os.getenv('OPENAI_API_KEY'))
        self.phone_features = PhoneFeatures()
        self.voice_manager = VoiceManager()
        
        # Tema renkleri
        self.bg_color = '#0a0e27'
        self.accent_color = '#FF1493'  # Pembe
        self.text_color = '#FFFFFF'
        
        self.setup_ui()
        self.load_contacts()
        
    def setup_ui(self):
        """Arayüzü kuruyor"""
        # Üst panel - Niko Avatar
        avatar_frame = tk.Frame(self.root, bg=self.bg_color)
        avatar_frame.pack(pady=20)
        
        avatar_label = tk.Label(
            avatar_frame,
            text="●",
            font=("Arial", 100),
            fg=self.accent_color,
            bg=self.bg_color
        )
        avatar_label.pack()
        
        name_label = tk.Label(
            avatar_frame,
            text="NIKO",
            font=("Arial", 20, "bold"),
            fg=self.text_color,
            bg=self.bg_color
        )
        name_label.pack()
        
        # Durum etiketi
        self.status_label = tk.Label(
            self.root,
            text="Hazırım, söyleyin!",
            font=("Arial", 12),
            fg=self.accent_color,
            bg=self.bg_color
        )
        self.status_label.pack()
        
        # Chat alanı
        chat_frame = tk.Frame(self.root, bg=self.bg_color)
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        self.chat_display = scrolledtext.ScrolledText(
            chat_frame,
            height=15,
            width=90,
            bg='#1a1f3a',
            fg=self.text_color,
            insertbackground=self.accent_color,
            font=("Arial", 10)
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)
        self.chat_display.config(state=tk.DISABLED)
        
        # Giriş alanı
        input_frame = tk.Frame(self.root, bg=self.bg_color)
        input_frame.pack(fill=tk.X, padx=20, pady=10)
        
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
        button_frame = tk.Frame(self.root, bg=self.bg_color)
        button_frame.pack(fill=tk.X, padx=20, pady=10)
        
        buttons = [
            ("🎤 Sesli", self.voice_input),
            ("📤 Gönder", self.send_message),
            ("📞 Ara", self.show_contacts),
            ("📅 Takvim", self.show_calendar),
            ("🌍 Arama", self.web_search),
            ("🎵 Müzik", self.play_music),
            ("📍 Harita", self.show_map),
            ("⚙️ Ayarlar", self.show_settings)
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
        self.status_label.config(text="Düşünüyorum...")
        
        # Thread'de işleme
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
                self.handle_weather(text)
            elif 'arama' in text_lower or 'araştır' in text_lower or 'internet' in text_lower:
                self.handle_web_search(text)
            else:
                # Tıbbi analiz
                response = self.niko_ai.analyze_symptoms(text)
                self.add_message("Niko", response)
        
        except Exception as e:
            self.add_message("Niko", f"Hata oluştu: {str(e)}")
        
        self.status_label.config(text="Hazırım, söyleyin!")
    
    def handle_call(self, text):
        """Telefon çalması"""
        contact_name = self.extract_contact(text)
        result = self.phone_features.make_call(contact_name)
        self.add_message("Niko", result)
    
    def handle_sms(self, text):
        """Mesaj gönderme"""
        contact_name = self.extract_contact(text)
        result = self.phone_features.send_sms(contact_name, text)
        self.add_message("Niko", result)
    
    def handle_calendar(self, text):
        """Takvim ve hatırlatıcı"""
        result = self.phone_features.add_reminder(text)
        self.add_message("Niko", result)
    
    def handle_timer(self, text):
        """Timer ve alarm"""
        result = self.phone_features.set_timer(text)
        self.add_message("Niko", result)
    
    def handle_music(self, text):
        """Müzik çalma"""
        result = self.phone_features.play_music(text)
        self.add_message("Niko", result)
    
    def handle_map(self, text):
        """Harita ve konum"""
        result = self.phone_features.find_location(text)
        self.add_message("Niko", result)
    
    def handle_weather(self, text):
        """Hava durumu"""
        result = self.phone_features.get_weather()
        self.add_message("Niko", result)
    
    def handle_web_search(self, text):
        """İnternet arama"""
        result = self.phone_features.web_search(text)
        self.add_message("Niko", result)
    
    def extract_contact(self, text):
        """Metinden kişi adı çıkarma"""
        # Basit implementasyon
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
            self.input_text.delete(0, tk.END)
            self.input_text.insert(0, text)
            self.root.after(100, self.send_message)
        except Exception as e:
            self.add_message("Niko", f"Ses tanıma hatası: {str(e)}")
            self.status_label.config(text="Hazırım, söyleyin!")
    
    def show_contacts(self):
        """Kişiler listesi gösterme"""
        self.add_message("Niko", "Kişileri gösteri") 
    
    def show_calendar(self):
        """Takvim gösterme"""
        self.input_text.insert(0, "Takvimi açar mısın?")
    
    def web_search(self):
        """Web arama başlatma"""
        self.input_text.insert(0, "Bunu araştır: ")
    
    def play_music(self):
        """Müzik çalma"""
        self.input_text.insert(0, "Müzik çal: ")
    
    def show_map(self):
        """Harita gösterme"""
        self.input_text.insert(0, "Yakındaki harita göster: ")
    
    def show_settings(self):
        """Ayarlar"""
        messagebox.showinfo("Ayarlar", "Ayarlar penceresine devam edilecek...")
    
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
