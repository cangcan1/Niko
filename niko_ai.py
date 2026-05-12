#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openai
from medical_db import MedicalDatabase

class NikoAI:
    """Niko AI - Tıbbi Asistan"""
    
    def __init__(self, api_key):
        openai.api_key = api_key
        self.medical_db = MedicalDatabase()
        
    def analyze_symptoms(self, symptoms_text):
        """Belirtileri analiz etme"""
        try:
            # Veritabanından kontrol et
            db_result = self.medical_db.search_disease(symptoms_text)
            if db_result:
                return f"💊 Tıbbi Analiz:\n{db_result}"
            
            # GPT-3'e sor
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "Sen Niko, bir tıbbi asistan yapay zekasısın. Kullanıcının belirtilerini analiz et, olası hastalıkları söyle, ama her zaman doktora gitmeyi öner."
                    },
                    {
                        "role": "user",
                        "content": f"Belirtilerim: {symptoms_text}"
                    }
                ],
                max_tokens=300,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        
        except Exception as e:
            return f"❌ Analiz hatası: {str(e)}"
    
    def get_medical_info(self, query):
        """Tıbbi bilgi alma"""
        return self.medical_db.get_info(query)
