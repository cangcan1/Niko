#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
from datetime import datetime

class WeatherDashboard:
    """Hava Durumu Gösterge Paneli"""
    
    def __init__(self):
        # OpenWeatherMap API (ücretsiz)
        self.api_key = "2d4b5aee0c2f5abfe5eeea6d23b05c45"  # Demo API key
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
        self.forecast_url = "https://api.openweathermap.org/data/2.5/forecast"
    
    def get_weather(self, city="Istanbul"):
        """Hava durumunu al"""
        try:
            # Güncel hava durumu
            params = {
                'q': city,
                'appid': self.api_key,
                'units': 'metric',
                'lang': 'tr'
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                return self.format_weather(data, city)
            else:
                return f"❌ {city} için hava durumu bilgisi bulunamadı.\n\n💡 İpucu: Şehir adını doğru yazın (örn: İstanbul, Ankara, İzmir)"
        
        except requests.exceptions.Timeout:
            return "⏱️ İnternet bağlantısı yavaş. Lütfen tekrar deneyin."
        except Exception as e:
            return f"❌ Hava durumu alırken hata: {str(e)}\n\n💡 Demo mod aktif. Gerçek API anahtarını ekleyin."
    
    def format_weather(self, data, city):
        """Hava durumu bilgisini formatla"""
        try:
            weather = data.get('main', {})
            description = data.get('weather', [{}])[0].get('description', 'Bilinmiyor')
            wind = data.get('wind', {})
            clouds = data.get('clouds', {})
            timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            
            # Emoji seçimi
            emoji_map = {
                'açık': '☀️',
                'bulutlu': '⛅',
                'yağmurlu': '🌧️',
                'kar': '❄️',
                'gök gürültü': '⛈️',
                'sis': '🌫️',
            }
            
            emoji = '🌤️'
            for key, value in emoji_map.items():
                if key in description.lower():
                    emoji = value
                    break
            
            weather_text = f"""
╔════════════════════════════════════════════════════════════════╗
║          🌍 {city.upper()} - HAVA DURUMU RAPORU                  ║
╚════════════════════════════════════════════════════════════════╝

📅 Tarih ve Saat: {timestamp}

🌡️  SICAKLIK BİLGİSİ:
  • Mevcut Sıcaklık: {weather.get('temp', 'N/A')}°C
  • Hissedilen Sıcaklık: {weather.get('feels_like', 'N/A')}°C
  • Minimum Sıcaklık: {weather.get('temp_min', 'N/A')}°C
  • Maksimum Sıcaklık: {weather.get('temp_max', 'N/A')}°C

💧 NEM VE BASKI:
  • Nem Oranı: {weather.get('humidity', 'N/A')}%
  • Hava Basıncı: {weather.get('pressure', 'N/A')} hPa

💨 RÜZGAR BİLGİSİ:
  • Rüzgar Hızı: {wind.get('speed', 'N/A')} m/s
  • Rüzgar Yönü: {wind.get('deg', 'N/A')}°
  • Rüzgar Eşeği: {wind.get('gust', 'N/A')} m/s

☁️ BULUTLULUK:
  • Bulut Yüzdesi: {clouds.get('all', 'N/A')}%

{emoji} HAVA DURUMU: {description.upper()}

═══════════════════════════════════════════════════════════════════

💡 ÖNERİLER:
"""
            
            # Sıcaklığa göre öneriler
            temp = weather.get('temp', 0)
            if temp < 0:
                weather_text += "  ❄️ Çok soğuk! Kalın giysiler giyin."
            elif temp < 10:
                weather_text += "  🧥 Soğuk hava. Mont giyiniz."
            elif temp < 20:
                weather_text += "  🌤️ Tempereli hava. Hafif kat giyin."
            elif temp < 30:
                weather_text += "  ☀️ Güzel hava. Dışarı çıkmak için ideal!"
            else:
                weather_text += "  🔥 Çok sıcak! Serin yerlerde kalın ve bol su için."
            
            # Yağmur uyarısı
            if 'yağmur' in description.lower() or 'sağanak' in description.lower():
                weather_text += "\n  🌧️ Yağmur bekleniyor! Şemsiye almayı unutmayın."
            
            # Rüzgar uyarısı
            if wind.get('speed', 0) > 10:
                weather_text += "\n  💨 Güçlü rüzgar! Dikkatli olun."
            
            weather_text += "\n\n═══════════════════════════════════════════════════════════════════"
            
            return weather_text
        
        except Exception as e:
            return f"❌ Hava durumu formatlanırken hata: {str(e)}"
