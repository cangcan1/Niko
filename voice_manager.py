#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import speech_recognition as sr
import pyttsx3

class VoiceManager:
    """Ses giriş/çıkış yönetimi"""
    
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.engine = pyttsx3.init()
        self.engine.setProperty('rate', 150)  # Konuşma hızı
        self.engine.setProperty('volume', 1)  # Ses seviyesi
    
    def listen(self):
        """Ses tanıma - Türkçe konuşmayı dinleme (timeout ile)"""
        try:
            with sr.Microphone() as source:
                print("🎤 Dinliyorum...")
                audio = self.recognizer.listen(source, timeout=5)
            
            # Google Speech Recognition kullanarak Türkçe
            text = self.recognizer.recognize_google(audio, language='tr-TR')
            print(f"Anladım: {text}")
            return text
        
        except sr.UnknownValueError:
            return "Anlamadım, lütfen tekrar söyleyin."
        except sr.RequestError:
            return "İnternet bağlantısı yok."
        except sr.exceptions.ReadTimeout:
            return ""
        except Exception as e:
            return f"Ses tanıma hatası: {str(e)}"
    
    def listen_without_timeout(self):
        """Ses tanıma - Timeout olmadan sürekli dinleme (arka plan)"""
        try:
            with sr.Microphone() as source:
                # Arka planda sürekli dinle, timeout yoktur
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=5)
            
            # Google Speech Recognition kullanarak Türkçe
            text = self.recognizer.recognize_google(audio, language='tr-TR')
            print(f"Anladım: {text}")
            return text
        
        except sr.UnknownValueError:
            return ""
        except sr.RequestError:
            return ""
        except sr.exceptions.ReadTimeout:
            return ""
        except Exception as e:
            print(f"Dinleme hatası: {str(e)}")
            return ""
    
    def speak(self, text):
        """Sesli konuşma - Türkçe metin seslendir"""
        try:
            # Türkçe karakterleri düzenle
            text = text.replace('ç', 'c').replace('ğ', 'g').replace('ı', 'i')
            text = text.replace('ö', 'o').replace('ş', 's').replace('ü', 'u')
            
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            print(f"Konuşma hatası: {str(e)}")
