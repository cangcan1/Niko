# 🤖 Niko - AI Tıbbi Asistan

**Cebinizde Bir Yapay Zeka Doktoru**

Niko, modern bir yapay zeka uygulamasıdır. Hastalık belirtilerinizi söyleyince analiz eder, teşhis önerileri sunar ve telefon gibi her şeyi yapabilir!

## 🎯 Temel Özellikler

### 🏥 Tıbbi Özellikler
- 💊 **Hastalık Analizi**: Belirtileri söyleyin, Niko tanı önerileri sunuyor
- 🧬 **Tıbbi Bilgi**: Binlerce hastalık ve semptomu kapsar
- 📋 **Hastalık Geçmişi**: Önceki sorgularınız kaydedilir
- ⚠️ **Uyarılar**: Ciddi durumlarda doktora gitmeyi önerir

### 📱 Telefon Özellikleri
- 🎤 **Sesli Komut**: Türkçe konuşma tanıma
- 📞 **Telefon Çalması**: Kişileri arayın
- 💬 **SMS Gönderme**: Mesaj gönderin
- 📅 **Takvim & Hatırlatıcılar**: Randevular ve görevleri not alın
- ⏰ **Timer/Alarm**: Zamanlayıcı ayarlayın
- 🎵 **Müzik Çalma**: Favori müziklerinizi dinleyin
- 📍 **Harita**: En yakın hastaneyi bulun
- 🌍 **Web Arama**: İnternet üzerinde araştırma yapın
- 🌤️ **Hava Durumu**: Güncel hava bilgisi
- 💻 **Todo List**: Görevleri yönetin

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- Mikrofon
- İnternet bağlantısı

### Adım 1: Repository'i Klonlayın
```bash
git clone https://github.com/cangcan1/Niko.git
cd Niko
```

### Adım 2: Paketleri Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 3: Çalıştırın
```bash
python main.py
```

## 🎤 Nasıl Kullanılır

### Sesli Komut
1. Uygulamayı çalıştırın
2. **"Niko" deyin**
3. Niko sesli cevap verir: "Buradayım, ne yardımcı olabilirim?"
4. Belirtilerinizi veya komutunuzu söyleyin
5. Niko sesli ve yazılı cevap verir

### Örnek Komutlar

#### Tıbbi
```
"Niko, başım ağrıyor"
"Niko, ateşim var, ne yapmalıyım?"
"Niko, boğaz ağrısı ve öksürük"
```

#### Telefon
```
"Annemi ara"
"Ali'ye mesaj gönder"
"5 dakika timer koy"
"Yarın doktor randevum var"
"Rahatlayıcı müzik çal"
"Yakındaki hastaneyi bul"
```

## 🎨 Arayüz

- 🖥️ **Sekmeler**: Chat, Todo List, Hava Durumu, Ayarlar
- 🎯 **Pembe Avatar**: Niko'nun karakteri
- 🌙 **Koyu Tema**: Gözlere hoş, modern tasarım
- 🎤 **Sesli Komut**: Tuşa basmadan çalışır
- 💬 **Chat Geçmişi**: Tüm konuşmalar kaydedilir

## 📁 Proje Yapısı

```
Niko/
├── main.py              # Ana uygulama (GUI + sekmeler)
├── niko_ai.py           # GPT-3 AI modülü
├── voice_manager.py     # Ses sistemi
├── phone_features.py    # Telefon özellikleri
├── medical_db.py        # Tıbbi hastalık veritabanı
├── todo_manager.py      # Todo List yöneticisi
├── weather_dashboard.py # Hava durumu paneli
├── requirements.txt     # Python paketleri
├── .env.example         # Ortam değişkenleri
├── contacts.json        # Kaydedilen kişiler
├── todos.json           # Görev listesi
└── README.md            # Bu dosya
```

## ⚙️ Konfigürasyon

### OpenAI API (Opsiyonel)

GPT-3 AI kullanmak için:

1. [OpenAI](https://platform.openai.com/api-keys) adresinden API anahtarı alın
2. `.env.example` dosyasını `.env` olarak kopyalayın
3. API anahtarınızı ekleyin:

```bash
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

## ⚠️ Önemli Not

**Niko tıbbi tavsiye değildir!** Ciddi durumlarda her zaman doktora başvurun.

- 🚑 Acil durumda 112'yi arayın
- 👨‍⚕️ Kalp ağrısı, nefes darlığı, ciddi yaralanmalar: Doktor
- 💊 İlaç alıyorsanız doktorunuza danışın

## 📊 Hava Durumu API

Niko, OpenWeatherMap API'sini kullanarak:
- 🌡️ Güncel sıcaklık
- 💧 Nem oranı
- 💨 Rüzgar hızı
- ☁️ Bulutluluk
- 🌧️ Yağmur tahmini

## 🎵 Müzik ve Harita

Niko şu servisleri entegre eder:
- 🎵 Spotify, YouTube Music
- 🗺️ Google Maps
- 📞 Kontaklar

## 🔒 Gizlilik

- 📱 Verileriniz yerel olarak saklanır
- 🔐 API anahtarınızı gizli tutun
- 🚫 Kişisel bilgilerinizi paylaşmayın
- 📝 Chat geçmişi cihazınızda saklanır

## 🐛 Sorun Giderme

### Ses tanıma çalışmıyor
- ✓ Mikrofonun bağlı olduğunu kontrol edin
- ✓ İnternet bağlantınızı kontrol edin
- ✓ Windows'ta: Ses ayarlarında mikrofon izni verin

### API hatası
- ✓ OpenAI API anahtarınızı kontrol edin
- ✓ Kullanım limitinizi aşmadığınızı kontrol edin
- ✓ İnternet bağlantısını kontrol edin

## 📚 Kaynaklar

- [OpenAI API Docs](https://platform.openai.com/docs)
- [Speech Recognition](https://pypi.org/project/SpeechRecognition/)
- [OpenWeatherMap API](https://openweathermap.org/api)
- [Google Maps](https://developers.google.com/maps)

## 📄 Lisans

MIT License - Özgürce kullanabilirsiniz

## 👨‍💻 Geliştirici

**Niko Projesi** - 2026

GitHub: [github.com/cangcan1/Niko](https://github.com/cangcan1/Niko)

---

**Niko'yu beğendiyseniz ⭐ vermeyi unutmayın!**
