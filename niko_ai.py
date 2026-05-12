#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import openai
from medical_db import MedicalDatabase

class NikoAI:
    """Niko AI - Tıbbi Asistan"""
    
    def __init__(self, api_key):
        if api_key and api_key != "demo":
            openai.api_key = api_key
        self.medical_db = MedicalDatabase()
        self.has_api = api_key and api_key != "demo"
        
    def analyze_symptoms(self, symptoms_text):
        """Belirtileri analiz etme"""
        try:
            # Veritabanından kontrol et
            db_result = self.medical_db.search_disease(symptoms_text)
            if db_result:
                return f"💊 Tıbbi Analiz:\n{db_result}"
            
            # Eğer API key varsa GPT-3'e sor
            if self.has_api:
                try:
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
                        max_tokens=200,
                        temperature=0.7
                    )
                    return response.choices[0].message.content
                except:
                    pass
            
            # Varsayılan cevap
            return f"💊 Belirtiler: {symptoms_text[:100]}\n\n⚠️ Bu belirtiler hakkında daha fazla bilgi almak için lütfen doktora başvurun.\n\n🏥 Yakındaki hastaneleri bulmak için 'Harita' butonunu kullanabilirsiniz."
        
        except Exception as e:
            return f"❌ Analiz hatası: {str(e)}"
