#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Kişisel Takvim Uygulaması
macOS için yerel takvim ve etkinlik yönetimi
"""

import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import json
import os
from datetime import datetime, timedelta
import calendar


class CalendarApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Kişisel Takvim")
        self.root.geometry("1200x800")

        # Veri dosyası
        self.data_file = "events.json"
        self.events = self.load_events()

        # Mevcut tarih
        self.current_date = datetime.now()
        self.selected_date = None

        # Renk şeması
        self.colors = {
            'etkinlik': '#4CAF50',
            'toplantı': '#2196F3',
            'görev': '#FF9800',
            'bg': '#f5f5f5',
            'today': '#FFE082',
            'selected': '#B3E5FC'
        }

        self.setup_ui()
        self.update_calendar()

    def load_events(self):
        """JSON dosyasından etkinlikleri yükle"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except:
                return {}
        return {}

    def save_events(self):
        """Etkinlikleri JSON dosyasına kaydet"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.events, f, ensure_ascii=False, indent=2)

    def setup_ui(self):
        """Kullanıcı arayüzünü oluştur"""
        # Ana container
        main_frame = tk.Frame(self.root, bg='white')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Sol panel - Takvim
        left_panel = tk.Frame(main_frame, bg='white')
        left_panel.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))

        # Takvim başlık
        header_frame = tk.Frame(left_panel, bg='white')
        header_frame.pack(fill=tk.X, pady=(0, 10))

        # Ay navigasyon butonları
        tk.Button(header_frame, text="◀", command=self.prev_month,
                 font=('Arial', 14), bg='#e0e0e0', relief=tk.FLAT, padx=15).pack(side=tk.LEFT, padx=5)

        self.month_label = tk.Label(header_frame, text="", font=('Arial', 18, 'bold'), bg='white')
        self.month_label.pack(side=tk.LEFT, expand=True)

        tk.Button(header_frame, text="▶", command=self.next_month,
                 font=('Arial', 14), bg='#e0e0e0', relief=tk.FLAT, padx=15).pack(side=tk.RIGHT, padx=5)

        tk.Button(header_frame, text="Bugün", command=self.goto_today,
                 font=('Arial', 11), bg='#2196F3', fg='white', relief=tk.FLAT, padx=10).pack(side=tk.RIGHT, padx=5)

        # Takvim grid
        self.calendar_frame = tk.Frame(left_panel, bg='white')
        self.calendar_frame.pack(fill=tk.BOTH, expand=True)

        # Sağ panel - Etkinlikler
        right_panel = tk.Frame(main_frame, bg='white', width=400)
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, padx=(10, 0))
        right_panel.pack_propagate(False)

        # Etkinlik başlık
        tk.Label(right_panel, text="Etkinlikler", font=('Arial', 16, 'bold'),
                bg='white').pack(pady=(0, 10))

        # Yeni etkinlik butonu
        tk.Button(right_panel, text="+ Yeni Etkinlik Ekle", command=self.add_event_dialog,
                 font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white',
                 relief=tk.FLAT, pady=10).pack(fill=tk.X, pady=(0, 20))

        # Seçili tarih etiketi
        self.selected_date_label = tk.Label(right_panel, text="Bir gün seçin",
                                           font=('Arial', 12), bg='white', fg='#666')
        self.selected_date_label.pack(pady=(0, 10))

        # Etkinlik listesi
        self.event_list_frame = tk.Frame(right_panel, bg='white')
        self.event_list_frame.pack(fill=tk.BOTH, expand=True)

        # Scrollable frame
        self.event_canvas = tk.Canvas(self.event_list_frame, bg='white', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.event_list_frame, orient="vertical", command=self.event_canvas.yview)
        self.scrollable_event_frame = tk.Frame(self.event_canvas, bg='white')

        self.scrollable_event_frame.bind(
            "<Configure>",
            lambda e: self.event_canvas.configure(scrollregion=self.event_canvas.bbox("all"))
        )

        self.event_canvas.create_window((0, 0), window=self.scrollable_event_frame, anchor="nw")
        self.event_canvas.configure(yscrollcommand=scrollbar.set)

        self.event_canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def update_calendar(self):
        """Takvim görünümünü güncelle"""
        # Önceki widget'ları temizle
        for widget in self.calendar_frame.winfo_children():
            widget.destroy()

        # Ay ve yıl etiketini güncelle
        month_name = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
                     'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']
        self.month_label.config(text=f"{month_name[self.current_date.month - 1]} {self.current_date.year}")

        # Gün başlıkları
        days = ['Pzt', 'Sal', 'Çar', 'Per', 'Cum', 'Cmt', 'Paz']
        for i, day in enumerate(days):
            tk.Label(self.calendar_frame, text=day, font=('Arial', 10, 'bold'),
                    bg='#e0e0e0', pady=5).grid(row=0, column=i, sticky='nsew', padx=1, pady=1)

        # Ayın günlerini hesapla
        cal = calendar.monthcalendar(self.current_date.year, self.current_date.month)

        today = datetime.now().date()

        for week_num, week in enumerate(cal):
            for day_num, day in enumerate(week):
                if day == 0:
                    # Boş gün
                    frame = tk.Frame(self.calendar_frame, bg='#f5f5f5', relief=tk.FLAT)
                    frame.grid(row=week_num + 1, column=day_num, sticky='nsew', padx=1, pady=1)
                else:
                    # Gerçek gün
                    date = datetime(self.current_date.year, self.current_date.month, day).date()
                    date_str = date.strftime('%Y-%m-%d')

                    # Arka plan rengi
                    bg_color = 'white'
                    if date == today:
                        bg_color = self.colors['today']

                    frame = tk.Frame(self.calendar_frame, bg=bg_color, relief=tk.RAISED, borderwidth=1)
                    frame.grid(row=week_num + 1, column=day_num, sticky='nsew', padx=1, pady=1)

                    # Gün numarası
                    tk.Label(frame, text=str(day), font=('Arial', 12, 'bold'),
                            bg=bg_color, fg='#333').pack(anchor='nw', padx=5, pady=5)

                    # Etkinlik sayısı
                    if date_str in self.events:
                        event_count = len(self.events[date_str])
                        tk.Label(frame, text=f"● {event_count}", font=('Arial', 9),
                                bg=bg_color, fg='#2196F3').pack(anchor='center')

                    # Tıklama eventi
                    frame.bind('<Button-1>', lambda e, d=date: self.select_date(d))
                    for child in frame.winfo_children():
                        child.bind('<Button-1>', lambda e, d=date: self.select_date(d))

        # Grid ağırlıkları
        for i in range(7):
            self.calendar_frame.columnconfigure(i, weight=1)
        for i in range(len(cal) + 1):
            self.calendar_frame.rowconfigure(i, weight=1)

    def select_date(self, date):
        """Tarih seçildiğinde"""
        self.selected_date = date
        date_str = date.strftime('%d %B %Y, %A')
        day_names = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma', 'Cumartesi', 'Pazar']
        month_names = ['Ocak', 'Şubat', 'Mart', 'Nisan', 'Mayıs', 'Haziran',
                      'Temmuz', 'Ağustos', 'Eylül', 'Ekim', 'Kasım', 'Aralık']

        formatted_date = f"{date.day} {month_names[date.month - 1]} {date.year}, {day_names[date.weekday()]}"
        self.selected_date_label.config(text=formatted_date, fg='#333', font=('Arial', 12, 'bold'))

        self.update_event_list()

    def update_event_list(self):
        """Seçili günün etkinliklerini göster"""
        # Önceki widget'ları temizle
        for widget in self.scrollable_event_frame.winfo_children():
            widget.destroy()

        if not self.selected_date:
            tk.Label(self.scrollable_event_frame, text="Bir gün seçin",
                    font=('Arial', 11), bg='white', fg='#999').pack(pady=20)
            return

        date_str = self.selected_date.strftime('%Y-%m-%d')

        if date_str not in self.events or len(self.events[date_str]) == 0:
            tk.Label(self.scrollable_event_frame, text="Bu gün için etkinlik yok",
                    font=('Arial', 11), bg='white', fg='#999').pack(pady=20)
            return

        # Etkinlikleri saate göre sırala
        events = sorted(self.events[date_str], key=lambda x: x.get('time', '00:00'))

        for idx, event in enumerate(events):
            event_frame = tk.Frame(self.scrollable_event_frame, bg='white',
                                  relief=tk.SOLID, borderwidth=1)
            event_frame.pack(fill=tk.X, pady=5, padx=5)

            # Renk çubuğu
            event_type = event.get('type', 'etkinlik')
            color_bar = tk.Frame(event_frame, bg=self.colors.get(event_type, '#4CAF50'), width=5)
            color_bar.pack(side=tk.LEFT, fill=tk.Y)

            # İçerik
            content_frame = tk.Frame(event_frame, bg='white')
            content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10, pady=10)

            # Saat ve başlık
            time_text = event.get('time', '')
            title_text = event.get('title', 'Başlıksız')
            tk.Label(content_frame, text=f"{time_text} - {title_text}",
                    font=('Arial', 12, 'bold'), bg='white', anchor='w').pack(anchor='w')

            # Tür
            tk.Label(content_frame, text=f"Tür: {event_type.capitalize()}",
                    font=('Arial', 9), bg='white', fg='#666', anchor='w').pack(anchor='w')

            # Açıklama
            if event.get('description'):
                tk.Label(content_frame, text=event['description'],
                        font=('Arial', 10), bg='white', fg='#333',
                        wraplength=250, anchor='w', justify=tk.LEFT).pack(anchor='w', pady=(5, 0))

            # Butonlar
            button_frame = tk.Frame(event_frame, bg='white')
            button_frame.pack(side=tk.RIGHT, padx=5)

            tk.Button(button_frame, text="✎", command=lambda e=event, i=idx: self.edit_event(e, i),
                     font=('Arial', 12), bg='#FFC107', fg='white',
                     relief=tk.FLAT, width=3).pack(side=tk.LEFT, padx=2)

            tk.Button(button_frame, text="✕", command=lambda i=idx: self.delete_event(i),
                     font=('Arial', 12), bg='#F44336', fg='white',
                     relief=tk.FLAT, width=3).pack(side=tk.LEFT, padx=2)

    def add_event_dialog(self):
        """Yeni etkinlik ekleme diyalogu"""
        if not self.selected_date:
            messagebox.showwarning("Uyarı", "Lütfen önce bir tarih seçin!")
            return

        dialog = tk.Toplevel(self.root)
        dialog.title("Yeni Etkinlik Ekle")
        dialog.geometry("500x450")
        dialog.resizable(False, False)

        # Modal yap
        dialog.transient(self.root)
        dialog.grab_set()

        main_frame = tk.Frame(dialog, bg='white', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Başlık
        tk.Label(main_frame, text="Yeni Etkinlik", font=('Arial', 16, 'bold'),
                bg='white').pack(pady=(0, 20))

        # Başlık girişi
        tk.Label(main_frame, text="Başlık:", font=('Arial', 11), bg='white',
                anchor='w').pack(fill=tk.X, pady=(0, 5))
        title_entry = tk.Entry(main_frame, font=('Arial', 12))
        title_entry.pack(fill=tk.X, pady=(0, 15))
        title_entry.focus()

        # Saat girişi
        tk.Label(main_frame, text="Saat (örn: 14:30):", font=('Arial', 11),
                bg='white', anchor='w').pack(fill=tk.X, pady=(0, 5))
        time_entry = tk.Entry(main_frame, font=('Arial', 12))
        time_entry.pack(fill=tk.X, pady=(0, 15))
        time_entry.insert(0, "09:00")

        # Tür seçimi
        tk.Label(main_frame, text="Tür:", font=('Arial', 11), bg='white',
                anchor='w').pack(fill=tk.X, pady=(0, 5))
        type_var = tk.StringVar(value="etkinlik")
        type_frame = tk.Frame(main_frame, bg='white')
        type_frame.pack(fill=tk.X, pady=(0, 15))

        for event_type in ['etkinlik', 'toplantı', 'görev']:
            tk.Radiobutton(type_frame, text=event_type.capitalize(), variable=type_var,
                          value=event_type, font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=10)

        # Açıklama
        tk.Label(main_frame, text="Açıklama:", font=('Arial', 11), bg='white',
                anchor='w').pack(fill=tk.X, pady=(0, 5))
        desc_text = tk.Text(main_frame, font=('Arial', 11), height=5, wrap=tk.WORD)
        desc_text.pack(fill=tk.X, pady=(0, 20))

        # Butonlar
        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(fill=tk.X)

        def save_event():
            title = title_entry.get().strip()
            time = time_entry.get().strip()

            if not title:
                messagebox.showwarning("Uyarı", "Lütfen bir başlık girin!")
                return

            # Saat formatını kontrol et
            try:
                datetime.strptime(time, '%H:%M')
            except:
                messagebox.showwarning("Uyarı", "Geçersiz saat formatı! Örnek: 14:30")
                return

            date_str = self.selected_date.strftime('%Y-%m-%d')

            if date_str not in self.events:
                self.events[date_str] = []

            new_event = {
                'title': title,
                'time': time,
                'type': type_var.get(),
                'description': desc_text.get('1.0', tk.END).strip()
            }

            self.events[date_str].append(new_event)
            self.save_events()
            self.update_calendar()
            self.update_event_list()

            dialog.destroy()
            messagebox.showinfo("Başarılı", "Etkinlik eklendi!")

        tk.Button(button_frame, text="Kaydet", command=save_event,
                 font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white',
                 relief=tk.FLAT, padx=30, pady=10).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="İptal", command=dialog.destroy,
                 font=('Arial', 12), bg='#e0e0e0', relief=tk.FLAT,
                 padx=30, pady=10).pack(side=tk.LEFT, padx=5)

    def edit_event(self, event, index):
        """Etkinlik düzenleme diyalogu"""
        dialog = tk.Toplevel(self.root)
        dialog.title("Etkinliği Düzenle")
        dialog.geometry("500x450")
        dialog.resizable(False, False)

        dialog.transient(self.root)
        dialog.grab_set()

        main_frame = tk.Frame(dialog, bg='white', padx=20, pady=20)
        main_frame.pack(fill=tk.BOTH, expand=True)

        tk.Label(main_frame, text="Etkinliği Düzenle", font=('Arial', 16, 'bold'),
                bg='white').pack(pady=(0, 20))

        # Başlık
        tk.Label(main_frame, text="Başlık:", font=('Arial', 11), bg='white',
                anchor='w').pack(fill=tk.X, pady=(0, 5))
        title_entry = tk.Entry(main_frame, font=('Arial', 12))
        title_entry.pack(fill=tk.X, pady=(0, 15))
        title_entry.insert(0, event.get('title', ''))

        # Saat
        tk.Label(main_frame, text="Saat (örn: 14:30):", font=('Arial', 11),
                bg='white', anchor='w').pack(fill=tk.X, pady=(0, 5))
        time_entry = tk.Entry(main_frame, font=('Arial', 12))
        time_entry.pack(fill=tk.X, pady=(0, 15))
        time_entry.insert(0, event.get('time', '09:00'))

        # Tür
        tk.Label(main_frame, text="Tür:", font=('Arial', 11), bg='white',
                anchor='w').pack(fill=tk.X, pady=(0, 5))
        type_var = tk.StringVar(value=event.get('type', 'etkinlik'))
        type_frame = tk.Frame(main_frame, bg='white')
        type_frame.pack(fill=tk.X, pady=(0, 15))

        for event_type in ['etkinlik', 'toplantı', 'görev']:
            tk.Radiobutton(type_frame, text=event_type.capitalize(), variable=type_var,
                          value=event_type, font=('Arial', 10), bg='white').pack(side=tk.LEFT, padx=10)

        # Açıklama
        tk.Label(main_frame, text="Açıklama:", font=('Arial', 11), bg='white',
                anchor='w').pack(fill=tk.X, pady=(0, 5))
        desc_text = tk.Text(main_frame, font=('Arial', 11), height=5, wrap=tk.WORD)
        desc_text.pack(fill=tk.X, pady=(0, 20))
        desc_text.insert('1.0', event.get('description', ''))

        button_frame = tk.Frame(main_frame, bg='white')
        button_frame.pack(fill=tk.X)

        def update_event():
            title = title_entry.get().strip()
            time = time_entry.get().strip()

            if not title:
                messagebox.showwarning("Uyarı", "Lütfen bir başlık girin!")
                return

            try:
                datetime.strptime(time, '%H:%M')
            except:
                messagebox.showwarning("Uyarı", "Geçersiz saat formatı! Örnek: 14:30")
                return

            date_str = self.selected_date.strftime('%Y-%m-%d')

            self.events[date_str][index] = {
                'title': title,
                'time': time,
                'type': type_var.get(),
                'description': desc_text.get('1.0', tk.END).strip()
            }

            self.save_events()
            self.update_calendar()
            self.update_event_list()

            dialog.destroy()
            messagebox.showinfo("Başarılı", "Etkinlik güncellendi!")

        tk.Button(button_frame, text="Güncelle", command=update_event,
                 font=('Arial', 12, 'bold'), bg='#4CAF50', fg='white',
                 relief=tk.FLAT, padx=30, pady=10).pack(side=tk.LEFT, padx=5)

        tk.Button(button_frame, text="İptal", command=dialog.destroy,
                 font=('Arial', 12), bg='#e0e0e0', relief=tk.FLAT,
                 padx=30, pady=10).pack(side=tk.LEFT, padx=5)

    def delete_event(self, index):
        """Etkinlik silme"""
        if messagebox.askyesno("Onay", "Bu etkinliği silmek istediğinizden emin misiniz?"):
            date_str = self.selected_date.strftime('%Y-%m-%d')
            del self.events[date_str][index]

            # Eğer gün boş kaldıysa, günü sil
            if len(self.events[date_str]) == 0:
                del self.events[date_str]

            self.save_events()
            self.update_calendar()
            self.update_event_list()
            messagebox.showinfo("Başarılı", "Etkinlik silindi!")

    def prev_month(self):
        """Önceki ay"""
        if self.current_date.month == 1:
            self.current_date = self.current_date.replace(year=self.current_date.year - 1, month=12)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month - 1)
        self.update_calendar()

    def next_month(self):
        """Sonraki ay"""
        if self.current_date.month == 12:
            self.current_date = self.current_date.replace(year=self.current_date.year + 1, month=1)
        else:
            self.current_date = self.current_date.replace(month=self.current_date.month + 1)
        self.update_calendar()

    def goto_today(self):
        """Bugüne git"""
        self.current_date = datetime.now()
        self.update_calendar()


def main():
    root = tk.Tk()
    app = CalendarApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
