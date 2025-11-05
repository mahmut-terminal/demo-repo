# 📅 Kişisel Takvim Uygulaması

macOS için tasarlanmış, tamamen yerel çalışan kişisel takvim ve etkinlik yönetimi uygulaması.

## ✨ Özellikler

- 📆 **Aylık Takvim Görünümü**: Tüm ayı bir bakışta görün
- ➕ **Etkinlik Yönetimi**: Etkinlik, toplantı ve görev ekleyin
- ⏰ **Saat Belirleme**: Her etkinlik için özel saat belirleyin
- 🎨 **Renkli Kategoriler**: Farklı etkinlik türleri için renk kodları
- ✏️ **Düzenleme**: Mevcut etkinlikleri kolayca güncelleyin
- 🗑️ **Silme**: İstenmeyen etkinlikleri kaldırın
- 💾 **Yerel Depolama**: Tüm veriler bilgisayarınızda JSON formatında saklanır
- 🔒 **Gizlilik**: İnternet bağlantısı gerektirmez, verileriniz cihazınızda kalır

## 🖥️ Sistem Gereksinimleri

- macOS (10.12 veya üzeri)
- Python 3.6+ (macOS'ta genellikle önceden yüklüdür)

## 🚀 Kurulum ve Çalıştırma

### 1. Python'un Yüklü Olduğunu Kontrol Edin

Terminal'i açın ve şu komutu çalıştırın:

```bash
python3 --version
```

Python 3.6 veya üzeri bir sürüm görmelisiniz. Eğer yüklü değilse, [python.org](https://www.python.org/downloads/) adresinden indirebilirsiniz.

### 2. Uygulamayı Çalıştırın

**EN KOLAY YOL** - Proje klasörüne gidin ve Python ile çalıştırın:

```bash
cd /Users/KULLANICI_ADINIZ/Desktop/takvim
python3 calendar_app.py
```

**Alternatif 1** - Başlatıcı Python scripti ile:

```bash
cd /Users/KULLANICI_ADINIZ/Desktop/takvim
python3 start.py
```

**Alternatif 2** - Bash scripti ile (Terminal kullanıcıları için):

```bash
cd /Users/KULLANICI_ADINIZ/Desktop/takvim
bash run.sh
```

veya çalıştırılabilir yapın:

```bash
chmod +x run.sh
./run.sh
```

**ÖNEMLİ**: `python3 run.sh` yazmayın! `run.sh` bir bash scriptidir, Python scripti değil.

### 3. Kolay Erişim için Alias Oluşturun (Opsiyonel)

Her seferinde klasöre gitmek istemiyorsanız, `.zshrc` veya `.bash_profile` dosyanıza şu satırı ekleyin:

```bash
alias takvim="python3 /tam/yol/demo-repo/calendar_app.py"
```

Sonra Terminal'den `takvim` yazarak uygulamayı açabilirsiniz.

## 📖 Kullanım Kılavuzu

### Temel Kullanım

1. **Tarih Seçme**: Takvimde bir güne tıklayın
2. **Etkinlik Ekleme**: "Yeni Etkinlik Ekle" butonuna basın
3. **Etkinlik Detayları**: Başlık, saat, tür ve açıklama girin
4. **Kaydetme**: "Kaydet" butonuna tıklayın

### Etkinlik Türleri

- **🎯 Etkinlik**: Genel etkinlikler (yeşil)
- **👥 Toplantı**: İş toplantıları ve görüşmeler (mavi)
- **✅ Görev**: Yapılacak işler ve görevler (turuncu)

### Etkinlik Düzenleme ve Silme

- **Düzenleme**: Etkinlik yanındaki **✎** (kalem) simgesine tıklayın
- **Silme**: Etkinlik yanındaki **✕** (çarpı) simgesine tıklayın

### Takvim Navigasyonu

- **◀ / ▶**: Önceki/sonraki aya git
- **Bugün**: Mevcut tarihe dön

## 💾 Veri Depolama

Tüm etkinlikleriniz `events.json` dosyasında saklanır. Bu dosya:

- Uygulamayla aynı klasörde bulunur
- İnsan tarafından okunabilir formattadır
- Yedeklenebilir (dosyayı kopyalayın)
- Elle düzenlenebilir (dikkatli olun!)

### Yedekleme

```bash
cp events.json events_backup.json
```

### Geri Yükleme

```bash
cp events_backup.json events.json
```

## 🎨 Ekran Görüntüsü Özellikleri

- **Sol Panel**: Aylık takvim görünümü
  - Bugünün tarihi sarı renkle vurgulanır
  - Etkinlik olan günlerde mavi nokta ve sayı gösterilir

- **Sağ Panel**: Seçili günün etkinlikleri
  - Renkli kategoriler
  - Saat sırasına göre listelenme
  - Hızlı düzenleme ve silme butonları

## 🔧 Sorun Giderme

### Uygulama Açılmıyor

**Çözüm 1**: Python yolunu kontrol edin
```bash
which python3
```

**Çözüm 2**: Tkinter'ın yüklü olduğunu kontrol edin
```bash
python3 -m tkinter
```
Küçük bir pencere açılmalıdır. Açılmazsa:
```bash
brew install python-tk@3.11
```

### events.json Bozuldu

Dosyayı silin, uygulama yeni bir tane oluşturacaktır:
```bash
rm events.json
```

### Türkçe Karakterler Düzgün Görünmüyor

Terminal encoding'inizi kontrol edin:
```bash
export LANG=tr_TR.UTF-8
```

## 📝 Özelleştirme

Uygulamayı özelleştirmek isterseniz `calendar_app.py` dosyasını düzenleyebilirsiniz:

- **Renkler**: `self.colors` sözlüğünü değiştirin (satır 29-35)
- **Pencere Boyutu**: `self.root.geometry()` değerini değiştirin (satır 23)
- **Varsayılan Saat**: `time_entry.insert()` değerini değiştirin (satır 244)

## 🤝 Katkıda Bulunma

Bu kişisel bir proje olduğu için önerilerinizi ve geri bildirimlerinizi memnuniyetle karşılarım!

## 📄 Lisans

Bu proje kişisel kullanım için oluşturulmuştur. Dilediğiniz gibi kullanabilir ve değiştirebilirsiniz.

## 🎯 Gelecek Özellikler (İsteğe Bağlı)

Eklemek isteyebileceğiniz özellikler:

- [ ] Tekrarlayan etkinlikler
- [ ] Hatırlatıcılar ve bildirimler
- [ ] Etkinlik arama
- [ ] İçe/dışa aktarma (iCal formatı)
- [ ] Haftalık görünüm
- [ ] Karanlık tema
- [ ] Etkinlik önceliklendirme

---

**Not**: Bu uygulama tamamen yerel çalışır ve hiçbir veri internete gönderilmez. Tüm bilgileriniz bilgisayarınızda güvende kalır.

Keyifle kullanın! 🎉
