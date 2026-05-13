#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
from datetime import datetime
import os

class TodoManager:
    """Todo/Görev yöneticisi"""
    
    def __init__(self, filename='todos.json'):
        self.filename = filename
        self.todos = self.load_todos()
    
    def load_todos(self):
        """Görevleri yükle"""
        try:
            with open(self.filename, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return []
    
    def save_todos(self):
        """Görevleri kaydet"""
        with open(self.filename, 'w', encoding='utf-8') as f:
            json.dump(self.todos, f, ensure_ascii=False, indent=2)
    
    def add_todo(self, text):
        """Görev ekle"""
        todo = {
            'text': text,
            'completed': False,
            'created_at': datetime.now().isoformat()
        }
        self.todos.append(todo)
        self.save_todos()
    
    def delete_todo(self, index):
        """Görev sil"""
        if 0 <= index < len(self.todos):
            self.todos.pop(index)
            self.save_todos()
    
    def toggle_todo(self, index):
        """Görev tamamlama durumunu değiştir"""
        if 0 <= index < len(self.todos):
            self.todos[index]['completed'] = not self.todos[index]['completed']
            self.save_todos()
    
    def get_todos(self):
        """Tüm görevleri al"""
        return self.todos
    
    def get_completed_count(self):
        """Tamamlanan görev sayısını al"""
        return sum(1 for todo in self.todos if todo['completed'])
    
    def clear_completed(self):
        """Tamamlanan görevleri temizle"""
        self.todos = [todo for todo in self.todos if not todo['completed']]
        self.save_todos()
