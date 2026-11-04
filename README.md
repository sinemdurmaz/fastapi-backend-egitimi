# 🚀 Python & FastAPI Profesyonel Backend Eğitimi

Bu depo; sıfırdan modern backend geliştirme, **RESTful API** standartları, **SQLite** veritabanı, **SQLModel (ORM)**, **JWT Tabanlı Kimlik Doğrulama (Auth)** ve **OOP (Nesne Yönelimli Programlama)** prensiplerini adım adım öğrenmek ve uygulamak için hazırlanmış kapsamlı bir referans projesidir.

---

## 🛠️ Kullanılan Teknolojiler ve Kütüphaneler

* **Python 3.15+**
* **[FastAPI](https://fastapi.tiangolo.com/):** Modern, yüksek performanslı web çatısı (Framework)
* **[SQLModel](https://sqlmodel.tiangolo.com/):** FastAPI & SQLAlchemy tabanlı ORM ve veri doğrulama kütüphanesi
* **[Uvicorn](https://www.uvicorn.org/):** Yıldırım hızında ASGI web sunucusu
* **[SQLite](https://www.sqlite.org/):** Hafif, dosya tabanlı ilişkisel veritabanı
* **[Pydantic](https://docs.pydantic.dev/):** Veri tipi kontrolü ve şema doğrulama
* **[pwdlib (Argon2)](https://github.com/frankie567/pwdlib):** Modern ve en yüksek güvenlikli şifre hashleme kütüphanesi
* **[PyJWT](https://pyjwt.readthedocs.io/):** Dijital imzalı JSON Web Token (JWT) oturum yönetimi
* **[python-dotenv](https://github.com/theskumar/python-dotenv):** `.env` dosyasından gizli çevre değişkenlerini okuma

---

## 📂 Proje Dizin Yapısı (Modüler Mimari)

```text
├── models.py         # Sınıflar, Pydantic şemaları, veritabanı modelleri & OOP ilişkileri
├── database.py       # SQLite motoru (Engine) ve tablo oluşturma fonksiyonu
├── security.py       # Argon2 şifre hashleme, JWT token üretimi ve doğrulama
├── main.py           # FastAPI uygulaması, bağımlılıklar (Depends) ve tüm uç noktalar (Endpoints)
├── .env.example      # Gizli anahtarlar için örnek çevre değişkenleri şablonu
├── README.md         # Proje vitrini ve dokümantasyonu
├── OOP_REHBERI.md    # Backend için sıfırdan OOP öğrenim rehberi
├── oop_rehberi.html  # OOP rehberinin karanlık mod interaktif web sayfası
└── yol_haritasi.html # Sıfırdan ileri seviye backend yol haritası ve takip paneli
```

---

## ✨ Projede Uygulanan Temel Özellikler

### 1. Kimlik Doğrulama & Güvenlik (Auth & Security)
* **Kullanıcı Kaydı (`/auth/kayit`):** Açık şifreler veritabanına asla yazılmaz; **Argon2** ile tek yönlü kırılmaz hash'e dönüştürülür. Çift e-posta kaydı engellenir.
* **Giriş Yapma (`/auth/giris`):** Şifre doğrulanırsa kullanıcıya mühürlü bir **JWT (JSON Web Token)** oturum bileti verilir.
* **Yetkilendirme & Rota Koruması (`Depends`):** Yazma/silme işlemleri `Depends(giris_yapmis_kullaniciyi_al)` bekçisiyle korunur. Token'ı olmayan istekler `401 Unauthorized` ile kapıda durdurulur.
* **Sahiplik (Ownership) Kontrolü:** Her eklenen ürün sahibinin `user_id` bilgisine mühürlenir. Başka bir kullanıcı ürününüzü silmeye veya güncellemeye çalışırsa sistem **`403 Forbidden`** hatası verir.
* **Gizli Anahtar Yönetimi (`.env`):** `SECRET_KEY` gibi kritik bilgiler kodun içine değil, `.gitignore` ile korunan `.env` dosyasına yazılır.

### 2. İlişkisel Veritabanı & OOP Gücü (One-to-Many Relationships)
* **Kategori & Ürün Bağlantısı:** Her ürün bir kategoriye bağlıdır (`kategori_id` - Foreign Key).
* **Nesneler Arası Doğrudan İletişim:** SQL sorgusu yazmadan:
  * `kategori.urunler` ➔ O kategoriye ait tüm ürünler listelenir.
  * `kullanici.urunler` ➔ Giriş yapan kullanıcının kendi eklediği ürünler listelenir.
  * `urun.sahip` ➔ Ürünün gerçek sahibi gelir.

### 3. OOP Kalıtım Hiyerarşisi & Kapsülleme
* `UrunBase` ata sınıfından türeyen `UrunCreate`, `Urun` ve `UrunUpdate` modelleri.
* Kullanıcı ürün eklerken `id` sorulmaz; veritabanı ID'yi otomatik üretir.
* `kdv_dahil_fiyat(self)` metodu ile nesnenin kendi fiyatı üzerinden dinamik KDV hesaplaması.

---

## 📋 API Uç Noktaları Tablosu (Endpoints)

| Kategori | Metot | Adres | Erişim | Açıklama |
| :--- | :--- | :--- | :--- | :--- |
| **Auth** | `POST` | `/auth/kayit` | Herkese Açık | Yeni kullanıcı kaydı (Şifreyi Argon2 ile hashler) |
| **Auth** | `POST` | `/auth/giris` | Herkese Açık | Giriş yapıp JWT Access Token alır |
| **Auth** | `GET` | `/auth/profil` | 🔒 Token Gerekir | Giriş yapan kullanıcının kendi profil bilgileri |
| **Auth** | `GET` | `/auth/urunlerim` | 🔒 Token Gerekir | Giriş yapan kullanıcının kendi eklediği ürünler |
| **Kategori**| `POST` | `/kategoriler` | 🔒 Token Gerekir | Yeni kategori oluşturur (Örn: "Elektronik") |
| **Kategori**| `GET` | `/kategoriler` | Herkese Açık | Tüm kategorileri listeler |
| **Kategori**| `GET` | `/kategoriler/{id}/urunler` | Herkese Açık | Belirli bir kategorinin altındaki tüm ürünleri getirir |
| **Ürün** | `POST` | `/urunler` | 🔒 Token Gerekir | Yeni ürün ekler (Sahiplik otomatik atanır) |
| **Ürün** | `GET` | `/urunler` | Herkese Açık | Tüm ürünleri listeler |
| **Ürün** | `GET` | `/urunler/{id}` | Herkese Açık | ID'si verilen ürünü detaylarıyla getirir |
| **Ürün** | `GET` | `/urunler/{id}/kdv` | Herkese Açık | Ürünün KDV dahil fiyatını hesaplar (OOP Metot Testi) |
| **Ürün** | `PATCH`| `/urunler/{id}` | 🔒 Sadece Sahibi | Ürünün istenen alanlarını günceller (403 Korumalı) |
| **Ürün** | `DELETE`| `/urunler/{id}` | 🔒 Sadece Sahibi | Ürünü veritabanından kalıcı olarak siler (403 Korumalı) |

---

## 🚀 Kurulum ve Çalıştırma

### 1. Depoyu Klonlayın
```bash
git clone https://github.com/sinemdurmaz/fastapi-backend-egitimi.git
cd fastapi-backend-egitimi
```

### 2. Sanal Ortamı Başlatın ve Paketleri Kurun
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install fastapi uvicorn sqlmodel "pwdlib[argon2]" pyjwt python-dotenv
```

### 3. Çevre Değişkenlerini (`.env`) Ayarlayın
```bash
cp .env.example .env
```
*(İsteğe bağlı olarak `.env` dosyasındaki `SECRET_KEY` değerini değiştirebilirsiniz).*

### 4. Sunucuyu Başlatın
```bash
uvicorn main:app --reload
```

Sunucu başladıktan sonra tarayıcınızdan interaktif Swagger dokümantasyonuna ulaşabilirsiniz:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

> 💡 **Swagger Test İpucu:** Korumalı uç noktaları test etmek için sağ üstteki **Authorize** butonuna tıklayıp `/auth/giris` adresinden aldığınız token'ı yapıştırmanız yeterlidir!

---

## 📚 Ek Dokümantasyonlar

* **[OOP_REHBERI.md](./OOP_REHBERI.md):** Backend geliştiriciler için sınıflar, `self`, `__init__`, kalıtım ve mimari rehberi.
* **[oop_rehberi.html](./oop_rehberi.html):** OOP kavramlarını görsel şemalarla anlatan interaktif karanlık mod web sayfası.
* **[yol_haritasi.html](./yol_haritasi.html):** Sıfırdan ileri seviye backend yol haritası ve ilerleme takip paneli.
