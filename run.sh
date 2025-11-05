#!/bin/bash
# Kişisel Takvim Uygulaması Başlatıcı

# Renk kodları
GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${BLUE}📅 Kişisel Takvim Uygulaması${NC}"
echo -e "${BLUE}================================${NC}\n"

# Python kontrolü
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 bulunamadı!${NC}"
    echo "Lütfen Python 3'ü yükleyin: https://www.python.org/downloads/"
    exit 1
fi

# Python versiyonu
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python $PYTHON_VERSION bulundu${NC}"

# Tkinter kontrolü
if ! python3 -c "import tkinter" 2>/dev/null; then
    echo -e "${RED}❌ Tkinter bulunamadı!${NC}"
    echo "Lütfen Tkinter'ı yükleyin: brew install python-tk@3.11"
    exit 1
fi

echo -e "${GREEN}✓ Tkinter bulundu${NC}"
echo -e "\n${GREEN}🚀 Uygulama başlatılıyor...${NC}\n"

# Uygulamayı başlat
python3 calendar_app.py

# Çıkış durumunu kontrol et
if [ $? -eq 0 ]; then
    echo -e "\n${GREEN}✓ Uygulama kapatıldı${NC}"
else
    echo -e "\n${RED}❌ Uygulama hata ile kapandı${NC}"
    exit 1
fi
