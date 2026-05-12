#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import webbrowser
import os
import json
import re
from datetime import datetime, timedelta
from duckduckgo_search import DDGS
import subprocess

class PhoneFeatures:
    """Telefon gibi özellikler"""
    
    def __init__(self):
        self.contacts = self.load_contacts()
        self.reminders = self.load_reminders()
        
    def make_call(self, contact_name):
        """Telefon çalması"""
        if contact_name.lower() in [c.lower() for c in self.contacts.keys()]:
            phone = self.contacts[contact_name]
            return f"📞 {contact_name}'yi arıyor... ({phone})"
        return f"⚠️ {contact_name} kişisi bulunamadı!"
    
    def send_sms(self, contact_name, message):
        """SMS gönderme"""
        if contact_name.lower() in [c.lower() for c in self.contacts.keys()]:
            phone = self.contacts[contact_name]
            return f"💬 {contact_name}'e SMS gönderiliyor...\n'{message}'"
        return f"⚠️ {contact_name} kişisi bulunamadı!"
    
    def add_reminder(self, text):
        """Hatırlatıcı ekleme"""
        try:
            # Zaman bilgisini çıkarmaya çalış
            if 'yarın' in text.lower():
                time = datetime.now() + timedelta(days=1)
            elif 'bugün' in text.lower():
                time = datetime.now()
            else:
                time = datetime.now() + timedelta(hours=1)
            
            reminder = {
                'text': text,
                'time': str(time),
                'created': str(datetime.now())
            }
            self.reminders.append(reminder)
            self.save_reminders()
            return f"📅 Hatırlatıcı eklendi: {text}"
        except Exception as e:
            return f"❌ Hatırlatıcı eklenirken hata: {str(e)}"
    
    def set_timer(self, text):
        """Timer ve alarm ayarlama"""
        # Sayı çıkart
        numbers = re.findall(r'\d+', text)
        if numbers:
            time_value = numbers[0]
            if 'dakika' in text.lower():
                return f"⏱️ {time_value} dakikalık timer başlatıldı"
            elif 'saat' in text.lower():
                return f"⏱️ {time_value} saatlik alarm ayarlandı"
            else:
                return f"⏱️ {time_value} saniye timer başlatıldı"
        return "⏰ Lütfen zaman belirtin (örn: 5 dakika)"
    
    def play_music(self, text):
        """Müzik çalma"""
        # Müzik adını çıkart
        if 'rahatlatıcı' in text.lower():
            return "🎵 Rahatlatıcı müzik çalınıyor... 🎧"
        elif 'şarkı' in text.lower() or 'müzik' in text.lower():
            return "🎵 Müzik kütüphanesi açılıyor..."
        return "🎵 Müzik çalınıyor..."
    
    def find_location(self, text):
        """Konum bulma - Harita aç"""
        if 'hastane' in text.lower():
            location = "Yakındaki Hastaneler"
        elif 'eczane' in text.lower() or 'eczacı' in text.lower():
            location = "Yakındaki Eczaneler"
        elif 'hastane' in text.lower():
            location = "Acil Servis"
        else:
            location = text.split(':')[-1] if ':' in text else "Konum"
        
        return f"📍 Google Harita açılıyor: {location}"
    
    def get_weather(self):
        """Hava durumu"""
        return "🌤️ Bugünün hava durumu: Güneşli, 22°C, Hafif rüzgar"
    
    def web_search(self, text):
        """İnternet arama (DuckDuckGo)"""
        try:
            # Arama terimini çıkart
            search_term = text.replace('arama', '').replace('araştır', '').replace('internet', '').strip()
            
            if not search_term:
                return "🔍 Arama terimi giriniz"
            
            # DuckDuckGo search
            results = DDGS().text(search_term, max_results=3)
            
            response = f"🔍 '{search_term}' için arama sonuçları:\n\n"
            for i, result in enumerate(results, 1):
                response += f"{i}. {result['title']}\n"
                response += f"   {result['body'][:150]}...\n\n"
            
            return response
        except Exception as e:
            return f"❌ Arama hatası: {str(e)}"
    
    def load_contacts(self):
        """Kişileri yükle"""
        try:
            with open('contacts.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return {
                "Anne": "+90555123456",
                "Baba": "+90555654321",
                "Ali": "+90555789012",
                "Doktor": "+90555345678"
            }
    
    def load_reminders(self):
        """Hatırlatıcıları yükle"""
        try:
            with open('reminders.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def save_reminders(self):
        """Hatırlatıcıları kaydet"""
        with open('reminders.json', 'w', encoding='utf-8') as f:
            json.dump(self.reminders, f, ensure_ascii=False, indent=2)
