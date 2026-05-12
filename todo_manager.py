#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime

class TodoManager:
    """Todo List Yöneticisi"""
    
    def __init__(self):
        self.file = 'todos.json'
        self.tasks = self.load_tasks()
    
    def load_tasks(self):
        """Görevleri yükle"""
        try:
            with open(self.file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except:
            return []
    
    def save_tasks(self):
        """Görevleri kaydet"""
        with open(self.file, 'w', encoding='utf-8') as f:
            json.dump(self.tasks, f, ensure_ascii=False, indent=2)
    
    def add_task(self, title):
        """Yeni görev ekle"""
        task = {
            'title': title,
            'completed': False,
            'created': datetime.now().isoformat()
        }
        self.tasks.append(task)
        self.save_tasks()
    
    def toggle_task(self, index):
        """Görevi tamamlanmış/tamamlanmamış işaretle"""
        if 0 <= index < len(self.tasks):
            self.tasks[index]['completed'] = not self.tasks[index]['completed']
            self.save_tasks()
    
    def delete_task(self, index):
        """Görevi sil"""
        if 0 <= index < len(self.tasks):
            self.tasks.pop(index)
            self.save_tasks()
    
    def get_tasks(self):
        """Tüm görevleri getir"""
        return self.tasks
    
    def get_completed_count(self):
        """Tamamlanan görev sayısı"""
        return sum(1 for task in self.tasks if task['completed'])
