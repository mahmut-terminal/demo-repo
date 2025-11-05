#!/bin/bash
# Kişisel Takvim Uygulaması Başlatıcı

echo "📅 Kişisel Takvim Uygulaması"
echo "================================"
echo ""

# Script'in bulunduğu dizine git
cd "$(dirname "$0")"

# Python kontrolü
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 bulunamadı!"
    echo "Lütfen Python 3'ü yükleyin: https://www.python.org/downloads/"
    exit 1
fi

# Python versiyonu
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python $PYTHON_VERSION bulundu"

# Tkinter kontrolü
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo "❌ Tkinter bulunamadı!"
    echo "Lütfen Tkinter'ı yükleyin: brew install python-tk@3.11"
    exit 1
fi

echo "✓ Tkinter bulundu"
echo ""
echo "🚀 Uygulama başlatılıyor..."
echo ""

# Uygulamayı başlat
python3 calendar_app.py

# Çıkış durumunu kontrol et
if [ $? -eq 0 ]; then
    echo ""
    echo "✓ Uygulama kapatıldı"
else
    echo ""
    echo "❌ Uygulama hata ile kapandı"
    exit 1
fi
