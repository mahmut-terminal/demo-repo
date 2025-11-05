#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Takvim Uygulaması Başlatıcı
Bu dosyayı çift tıklayarak veya python3 start.py komutuyla çalıştırabilirsiniz.
"""

import sys
import subprocess

def check_tkinter():
    """Tkinter'ın yüklü olup olmadığını kontrol et"""
    try:
        import tkinter
        return True
    except ImportError:
        return False

def main():
    print("📅 Kişisel Takvim Uygulaması")
    print("=" * 32)
    print()

    # Python versiyonu
    python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
    print(f"✓ Python {python_version}")

    # Tkinter kontrolü
    if not check_tkinter():
        print("❌ Tkinter bulunamadı!")
        print("Lütfen Tkinter'ı yükleyin:")
        print("  brew install python-tk@3.11")
        sys.exit(1)

    print("✓ Tkinter bulundu")
    print()
    print("🚀 Uygulama başlatılıyor...")
    print()

    # Uygulamayı başlat
    try:
        from calendar_app import main as run_app
        run_app()
    except KeyboardInterrupt:
        print("\n\n✓ Uygulama kapatıldı")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Hata: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
