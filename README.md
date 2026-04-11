# 🔐 Güvenli Uzaktan Yönetim Sistemi (Python)

## 📌 Proje Hakkında

Bu proje, Python ile geliştirilmiş **istemci-sunucu (client-server) mimarisine sahip bir uzaktan yönetim sistemidir**.

Amaç, siber güvenlik ve ağ programlama alanlarında:

* güvenli veri iletişimi
* şifreli haberleşme
* uzaktan komut çalıştırma

gibi konuları pratik olarak öğrenmektir.

---

## 🚀 Özellikler

* 🔗 Çoklu istemci (multi-client) desteği
* 🔐 Fernet ile şifrelenmiş iletişim
* 💻 Uzaktan komut çalıştırma
* 📁 Dosya gönderme ve alma (upload/download)
* 🔄 Otomatik yeniden bağlantı (client tarafında)
* 🧠 Basit komut yönetim sistemi

---

## 🏗️ Mimari Yapı

```id="a91kdl"
project/
├── server.py   # Komut gönderme ve yönetim tarafı
├── client.py   # İstemci tarafı
```

### Çalışma Mantığı:

1. İstemci sunucuya bağlanır
2. Sunucu şifreleme anahtarı gönderir
3. Tüm veri şifreli olarak iletilir
4. Komutlar çalıştırılır ve sonuç geri gönderilir

---

## 🛠️ Kullanılan Teknolojiler

* Python 3
* Socket programlama
* cryptography (Fernet)
* Threading

---

## ⚙️ Kullanım

### 1. Gerekli kütüphane:

```bash
pip install cryptography
```

### 2. Sunucuyu başlat:

```bash
python server.py <ip> <port>
```

### 3. İstemciyi çalıştır:

`client.py` içinde IP adresini düzenledikten sonra:

```bash
python client.py
```

---

## 📖 Örnek Komutlar

```id="d8xk31"
list                # Bağlı istemcileri listele
use <id>            # İstemci seç
cd <klasör>         # Dizin değiştir
download <dosya>    # İstemciden dosya indir
upload <dosya>      # İstemciye dosya gönder
```

---

## ⚠️ Uyarı

Bu proje **yalnızca eğitim ve öğrenme amaçlı geliştirilmiştir.**

Yetkisiz sistemlerde kullanımı:

* etik değildir
* yasal sorunlara yol açabilir


