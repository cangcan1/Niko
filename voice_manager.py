#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import speech_recognition as sr
import pyttsx3

class VoiceManager:
    """Ses giriş/çıkış yönetimi"""
    
    def __init__(self):
        try:
            self.recognizer = sr.Recognizer()
            self.engine = pyttsx3.init()
            self.engine.setProperty('rate', 150)
            self.engine.setProperty('volume', 1)
        except:
            self.recognizer = None
            self.engine = None
    
    def listen(self):
        """Ses tanıma - Türkçe konuşmayı dinleme (timeout ile)"""
        if not self.recognizer:
            return "Ses sistemi başarısız oldu."
        
        try:
            with sr.Microphone() as source:
                print("🎤 Dinliyorum...")
                audio = self.recognizer.listen(source, timeout=5)
            
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
            return ""
    
    def listen_without_timeout(self):
        """Ses tanıma - Timeout olmadan sürekli dinleme (arka plan)"""
        if not self.recognizer:
            return ""
        
        try:
            with sr.Microphone() as source:
                audio = self.recognizer.listen(source, timeout=None, phrase_time_limit=5)
            
            text = self.recognizer.recognize_google(audio, language='tr-TR')
            print(f"Anladım: {text}")
            return text
        
        except:
            return ""
    
    def speak(self, text):
        """Sesli konuşma - Türkçe metin seslendir"""
        if not self.engine:
            return
        
        try:
            text = text.replace('ç', 'c').replace('ğ', 'g').replace('ı', 'i')
            text = text.replace('ö', 'o').replace('ş', 's').replace('ü', 'u')
            
            self.engine.say(text)
            self.engine.runAndWait()
        except:
            pass
