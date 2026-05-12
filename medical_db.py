#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class MedicalDatabase:
    """Tıbbi Hastalık Veritabanı"""
    
    def __init__(self):
        self.diseases = {
            'grip': {
                'symptoms': ['ateş', 'öksürük', 'burun tıkanıklığı', 'halsizlik'],
                'description': '🦠 Grip (Influenza): Viral bir enfeksiyon. Belirtiler: ateş (38-40°C), öksürük, burun akıntısı, halsizlik, kas ağrıları.',
                'advice': '✅ Bol su içiniz, dinlenin. İbuprofenle ateşi düşürün. 3-5 gün içinde geçmelidir. Eğer kötüye giderse doktora gidin.'
            },
            'soğuk alğınlığı': {
                'symptoms': ['öksürük', 'burun tıkanıklığı', 'boğaz ağrısı'],
                'description': '🤧 Soğuk Alğınlığı: Viral enfeksiyon. Belirtiler: burun tıkanıklığı, öksürük, boğaz ağrısı, çoğunlukla ateş yoktur.',
                'advice': '✅ Sıcak çay için, madu ekleyin. Bol su içiniz. Genellikle 3-7 günde geçer.'
            },
            'baş ağrısı': {
                'symptoms': ['baş ağrısı', 'zonklama', 'başın zonklaması'],
                'description': '🤕 Baş Ağrısı: Stres, dehydrasyon, uyku yetersizliği nedeniyle olabilir.',
                'advice': '✅ Dinlenin, bol su içiniz. Parasetamol alınız. Koyu ortamda yatın. Eğer devam ederse doktora gidin.'
            },
            'boğaz ağrısı': {
                'symptoms': ['boğaz ağrısı', 'yutarken ağrı', 'iltihap'],
                'description': '😷 Boğaz Ağrısı: Viral veya bakteriyel enfeksiyon. Tonsillitler çok yaygındır.',
                'advice': '✅ Tuz suyuyla gargara yapın. Sıcak çay için. Antibiyotik gerekebilir - doktora danışın.'
            },
            'mide ağrısı': {
                'symptoms': ['mide krampları', 'bulantı', 'indirim iştahı'],
                'description': '🤢 Mide Ağrısı: Gastroenterit veya sindirim problemi olabilir.',
                'advice': '✅ Beslenme değiştirin (hafif yemekler). Probiyotik alınız. Bol su içiniz. 24-48 saat içinde geçmelidir.'
            },
            'ateş': {
                'symptoms': ['ateş', 'sıcaklık', 'titreme'],
                'description': '🌡️ Ateş: Vücudun enfeksiyonla mücadele işareti. Normal ateş 36.5-37.5°C arasıdır.',
                'advice': '✅ Parasetamol (500mg) veya İbuprofenin (400mg) alınız. Bol su içiniz. 38°C üzerinde doktora gidin.'
            },
            'öksürük': {
                'symptoms': ['öksürük', 'boğaz ağrısı', 'balgam'],
                'description': '🤐 Öksürük: Genellikle viral enfeksiyondan kaynaklanır.',
                'advice': '✅ Sıcak çay içiniz. Madu ekleyin. Öksürük şurubu alınız. Eğer 2 hafta devam ederse doktora gidin.'
            }
        }
    
    def search_disease(self, symptoms_text):
        """Hastalık arama"""
        text_lower = symptoms_text.lower()
        
        for disease_name, disease_info in self.diseases.items():
            if disease_name in text_lower:
                return f"{disease_info['description']}\n\n{disease_info['advice']}"
            
            for symptom in disease_info['symptoms']:
                if symptom in text_lower:
                    return f"{disease_info['description']}\n\n{disease_info['advice']}"
        
        return None
    
    def get_info(self, query):
        """Bilgi alma"""
        query_lower = query.lower()
        if query_lower in self.diseases:
            disease = self.diseases[query_lower]
            return f"{disease['description']}\n\n{disease['advice']}"
        return "Hastalık bulunamadı."
