# 🤖 Niko - AI Tıbbi Asistan

**Cebinizdeki Kişisel Doktor**

Niko, modern bir yapay zeka uygulamasıdır. Hastalık belirtilerinizi söyleyince analiz eder, teşhis önerileri sunar. Aynı zamanda bir smartphone gibi her şeyi yapabilir!

## 🎯 Temel Özellikler

### 🏥 Tıbbi Özellikler
- 💊 **Hastalık Analizi**: Belirtileri söyleyin, Niko tanı önerileri sunsun
- 🩺 **Tıbbi Bilgi**: Binlerce hastalık ve semptomu kapsar
- 📋 **Hastalık Geçmişi**: Önceki sorgularınız kaydedilir
- ⚠️ **Uyarılar**: Ciddi durumlarda doktora gitmeyi önerir

### 📱 Telefon Özellikleri
- 🎤 **Sesli Komut**: Türkçe konuşma tanıma
- 📞 **Telefon Çalması**: Kişileri arayın
- 💬 **SMS Gönderme**: Mesaj gönderin
- 📅 **Takvim & Hatırlatıcı**: Randevuları not alın
- ⏰ **Timer/Alarm**: Zamanlayıcı ayarlayın
- 🎵 **Müzik Çalma**: Favori müziklerinizi dinleyin
- 📍 **Harita**: En yakın hastaneyi bulun
- 🌍 **Web Arama**: İnternet üzerinde araştırma yapın
- 🌤️ **Hava Durumu**: Güncel hava bilgisi
- 📧 **Email Gönderme**: Mesaj gönder

## 🚀 Kurulum

### Gereksinimler
- Python 3.8+
- Mikrofon (sesli komut için)
- İnternet bağlantısı
- OpenAI API Anahtarı

### Adım 1: Repository'i Klonlayın
```bash
git clone https://github.com/cangcan1/Niko.git
cd Niko
```

### Adım 2: Bağımlılıkları Yükleyin
```bash
pip install -r requirements.txt
```

### Adım 3: API Anahtarını Ayarlayın
```bash
cp .env.example .env
```

`.env` dosyasını açıp OpenAI API anahtarınızı ekleyin:
```
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxx
```

### Adım 4: Çalıştırın
```bash
python main.py
```

## 💬 Kullanım Örnekleri

### Tıbbi Sorular
```
"Baş ağrım var, ne olabilir?"
"Ateşim var, ne yapmalıyım?"
"Boğaz ağrısı ve öksürük, grip mi?"
```

### Telefon Özellikleri
```
"Annemi ara"
"Ali'ye mesaj gönder"
"5 dakika timer koy"
"Yarın doktor randevum var"
"Rahatlatıcı müzik çal"
"Yakındaki hastaneyi bul"
"Baş ağrısı hakkında araştır"
```

## 🎨 Arayüz

- 🎯 Pembe parlak avatar (Niko)
- 🖤 Koyu tema (göz dostu)
- 📱 Mobil benzeri layout
- 🎤 Sesli komut butonu
- 💬 Yazılı giriş alanı
- 📊 Chat geçmişi

## 🔧 Dosya Yapısı

```
Niko/
├── main.py              # Ana uygulama ve GUI
├── niko_ai.py           # GPT-3 AI modülü
├── phone_features.py    # Telefon özellikleri
├── voice_manager.py     # Ses giriş/çıkış
├── medical_db.py        # Tıbbi hastalık veritabanı
├── requirements.txt     # Python paketleri
├── .env.example         # Ortam değişkenleri
├── contacts.json        # Kaydedilen kişiler
├── reminders.json       # Hatırlatıcılar
└── README.md            # Bu dosya
```

## ⚠️ Önemli

**Niko tıbbi tavsiye değildir!** Ciddi durumlarda her zaman doktora başvurun.

## 🔐 Gizlilik

- Verileriniz yerel olarak saklanır
- OpenAI API'ye gönderilen veriler OpenAI'nin gizlilik politikasına tabi
- API anahtarını hiç kimseyle paylaşmayın

## 🐛 Sorun Giderme

### Ses tanıma çalışmıyor
- Mikrofonun bağlı olduğunu kontrol edin
- İnternet bağlantınızı kontrol edin
- Windows: Ses ayarlarında mikrofon izni verin

### API hatası
- OpenAI API anahtarınızı kontrol edin
- Kullanım limitinizi aşmadığınızı kontrol edin

## 📚 Kaynaklar

- [OpenAI API Docs](https://platform.openai.com/docs)
- [Speech Recognition](https://pypi.org/project/SpeechRecognition/)
- [pyttsx3 Docs](https://pyttsx3.readthedocs.io/)

## 📄 Lisans

MIT License - Özgürce kullanabilirsiniz

## 👨‍💻 Geliştirici

**Niko Projesi** - 2026

---

**Niko'yu beğendiyseniz ⭐ vermeyi unutmayın!**
