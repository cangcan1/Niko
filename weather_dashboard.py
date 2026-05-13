#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
from datetime import datetime

class WeatherDashboard:
    """Hava durumu paneli"""
    
    def __init__(self):
        # Ücretsiz API kullan (API anahtarı gerekmiyor)
        self.weather_api = "https://open-meteo.com/en/docs"
        self.base_url = "https://api.open-meteo.com/v1/forecast"
        self.geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    
    def get_coordinates(self, city):
        """Şehrin koordinatlarını al"""
        try:
            params = {
                'name': city,
                'count': 1,
                'language': 'en'
            }
            response = requests.get(self.geo_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            if 'results' in data and len(data['results']) > 0:
                result = data['results'][0]
                return {
                    'latitude': result['latitude'],
                    'longitude': result['longitude'],
                    'name': result.get('name', city),
                    'country': result.get('country', '')
                }
            return None
        except Exception as e:
            print(f"Koordinat hatası: {e}")
            return None
    
    def get_weather(self, city):
        """Hava durumunu getir"""
        try:
            # Koordinatları al
            coords = self.get_coordinates(city)
            if not coords:
                return f"❌ '{city}' şehri bulunamadı!"
            
            # Hava verisi al
            params = {
                'latitude': coords['latitude'],
                'longitude': coords['longitude'],
                'current': 'temperature_2m,weather_code,wind_speed_10m,relative_humidity_2m',
                'daily': 'weather_code,temperature_2m_max,temperature_2m_min',
                'timezone': 'auto'
            }
            
            response = requests.get(self.base_url, params=params, timeout=5)
            response.raise_for_status()
            data = response.json()
            
            # Hava kodu açıklaması
            weather_codes = {
                0: '☀️ Açık',
                1: '🌤️ Hafif bulutlu',
                2: '⛅ Açık bulutlu',
                3: '☁️ Bulutlu',
                45: '🌫️ Sisli',
                48: '🌫️ Sis (Kırağı)',
                51: '🌧️ Hafif çisenti',
                53: '🌧️ Çisenti',
                55: '🌧️ Yoğun çisenti',
                61: '🌧️ Hafif yağmur',
                63: '🌧️ Yağmur',
                65: '🌧️ Yoğun yağmur',
                71: '❄️ Hafif kar',
                73: '❄️ Kar',
                75: '❄️ Yoğun kar',
                77: '❄️ Kar taneleri',
                80: '🌧️ Hafif sağanak',
                81: '🌧️ Sağanak',
                82: '🌧️ Yoğun sağanak',
                85: '🌨️ Hafif kar sağanağı',
                86: '🌨️ Kar sağanağı',
                95: '⛈️ Gök gürültülü',
                96: '⛈️ Gök gürültü + dolu',
                99: '⛈️ Gök gürültü + kar'
            }
            
            current = data.get('current', {})
            daily = data.get('daily', {})
            
            weather_code = current.get('weather_code', 0)
            weather_desc = weather_codes.get(weather_code, '❓ Bilinmiyor')
            
            # Formatlı çıktı
            output = f"""
╔══════════════════════════════════════════════════════════╗
║ 🌍 {coords['name'].upper()}, {coords['country']}
╚═══════════════���══════════════════════════════════════════╝

📍 Konum: Lat {coords['latitude']}, Lon {coords['longitude']}
🕐 Güncelleme: {datetime.now().strftime('%d.%m.%Y %H:%M:%S')}

━━━━━━━━━━━━━━━━━━ GÜNCEL HAVA ━━━━━━━━━━━━━━━━━━

🌡️  Sıcaklık: {current.get('temperature_2m', 'N/A')}°C
{weather_desc}
💨 Rüzgar Hızı: {current.get('wind_speed_10m', 'N/A')} km/s
💧 Nem: {current.get('relative_humidity_2m', 'N/A')}%

━━━━━━━━━━━━━━━━━━ GÜNLÜKür ━━━━━━━━━━━━━━━━━━
"""
            
            # Günlük tahminler
            if 'time' in daily:
                for i in range(min(3, len(daily['time']))):
                    date = daily['time'][i]
                    max_temp = daily['temperature_2m_max'][i]
                    min_temp = daily['temperature_2m_min'][i]
                    code = daily['weather_code'][i]
                    desc = weather_codes.get(code, '❓')
                    
                    output += f"\n📅 {date}\n"
                    output += f"   🔥 Max: {max_temp}°C | ❄️ Min: {min_temp}°C\n"
                    output += f"   {desc}\n"
            
            output += "\n" + "="*60
            return output
        
        except requests.exceptions.Timeout:
            return "❌ İstek zaman aşımına uğradı. İnternet bağlantınızı kontrol edin."
        except requests.exceptions.ConnectionError:
            return "❌ İnternet bağlantısı yok!"
        except Exception as e:
            return f"❌ Hava durumu hatası: {str(e)}"
