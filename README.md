# 🚀 Python & FastAPI Backend Eğitimi

Bu depo; sıfırdan modern backend geliştirme, **RESTful API** standartları, **SQLite** veritabanı, **SQLModel (ORM)** ve **OOP (Nesne Yönelimli Programlama)** prensiplerini adım adım öğrenmek ve uygulamak için hazırlanmış bir eğitim ve referans projesidir.

---

## 🛠️ Kullanılan Teknolojiler ve Kütüphaneler

* **Python 3.15+**
* **[FastAPI](https://fastapi.tiangolo.com/):** Modern, yüksek performanslı web framework'ü
* **[SQLModel](https://sqlmodel.tiangolo.com/):** FastAPI & SQLAlchemy tabanlı ORM ve veri doğrulama kütüphanesi
* **[Uvicorn](https://www.uvicorn.org/):** Yıldırım hızında ASGI web sunucusu
* **[SQLite](https://www.sqlite.org/):** Hafif, dosya tabanlı ilişkisel veritabanı
* **[Pydantic](https://docs.pydantic.dev/):** Veri tipi kontrolü ve doğrulama

---

## ✨ Projede Uygulanan Temel Özellikler

1. **Tam CRUD Döngüsü:**
   * **C**reate: `POST /urunler` (Yeni ürün kaydı)
   * **R**ead: `GET /urunler` ve `GET /urunler/{urun_id}` (Tümünü ve ID ile tek ürün listeleme)
   * **U**pdate: `PATCH /urunler/{urun_id}` (Kısmi güncelleme)
   * **D**elete: `DELETE /urunler/{urun_id}` (Veritabanından ürün silme)

2. **OOP (Nesne Yönelimli Programlama) Mimarisi:**
   * **Kalıtım Hiyerarşisi:** `UrunBase` ata sınıfından türeyen `UrunCreate`, `Urun` ve `UrunUpdate` sınıfları.
   * **Kapsülleme & Metotlar (`self`):** Nesnenin kendi verisi üzerinden KDV hesaplayan `kdv_dahil_fiyat()` metodu (`GET /urunler/{urun_id}/kdv`).
   * **Gereksiz Alanların Engellenmesi:** Kullanıcıdan ürün eklerken `id` istenmez; veritabanı ID'yi otomatik üretir.

3. **Veri Kalıcılığı (Database Persistence):**
   * Veriler geçici bellek (RAM) yerine yerel `veritabani.db` SQLite dosyasında saklanır. Sunucu kapansa bile veriler kaybolmaz.

4. **Otomatik API Dokümantasyonu (Swagger UI):**
   * Kod yazıldığı anda interaktif test arayüzü otomatik olarak `/docs` altında üretilir.

---

## 📋 API Uç Noktaları (Endpoints)

| Metot | Adres | Açıklama |
| :--- | :--- | :--- |
| `GET` | `/urunler` | Veritabanındaki tüm ürünleri listeler |
| `GET` | `/urunler/{urun_id}` | ID'si verilen ürünü detaylarıyla getirir (Yoksa 404 döner) |
| `GET` | `/urunler/{urun_id}/kdv` | Ürünün KDV dahil fiyatını hesaplar (OOP metot testi) |
| `POST` | `/urunler` | Yeni bir ürün ekler (`isim`, `fiyat`, `stokta_var_mi`) |
| `PATCH`| `/urunler/{urun_id}` | Ürünün istenen alanlarını günceller |
| `DELETE`| `/urunler/{urun_id}` | Ürünü veritabanından kalıcı olarak siler |

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
pip install fastapi uvicorn sqlmodel
```

### 3. Sunucuyu Başlatın
```bash
uvicorn main:app --reload
```

Sunucu başladıktan sonra tarayıcınızdan interaktif API dokümantasyonuna ulaşabilirsiniz:
👉 **[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)**

---

## 📚 Ek Dokümantasyonlar

* **[OOP_REHBERI.md](./OOP_REHBERI.md):** Backend geliştiriciler için sınıflar, `self`, `__init__`, kalıtım ve mimari rehberi.
* **[oop_rehberi.html](./oop_rehberi.html):** OOP kavramlarını görsel ve interaktif olarak anlatan karanlık mod web sayfası.
* **[yol_haritasi.html](./yol_haritasi.html):** Sıfırdan ileri seviye backend yol haritası ve ilerleme takip paneli.
