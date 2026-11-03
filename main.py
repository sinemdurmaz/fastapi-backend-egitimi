from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

from database import engine, veritabanini_olustur
from models import (
    Kategori,
    KategoriCreate,
    Kullanici,
    KullaniciCreate,
    KullaniciPublic,
    Urun,
    UrunCreate,
    UrunUpdate,
)
from security import sifre_hashle


@asynccontextmanager
async def omur_dongusu(app: FastAPI):
    veritabanini_olustur()
    yield


app = FastAPI(title="OOP, Auth & Güvenlik Destekli API", lifespan=omur_dongusu)


# ==========================================
# KİMLİK DOĞRULAMA (AUTH) UÇ NOKTALARI
# ==========================================


# 1. YENİ KULLANICI KAYDI (REGISTER)
@app.post("/auth/kayit", response_model=KullaniciPublic)
def kullanici_kayit(kullanici_verisi: KullaniciCreate):
    with Session(engine) as session:
        # Aynı e-posta daha önce alınmış mı?
        mevcut_kullanici = session.exec(
            select(Kullanici).where(Kullanici.email == kullanici_verisi.email)
        ).first()
        if mevcut_kullanici:
            raise HTTPException(status_code=400, detail="Bu e-posta adresi zaten kullanımda!")

        # Şifreyi kırılmaz bir Argon2 hash'ine dönüştürüyoruz
        guvenli_sifre = sifre_hashle(kullanici_verisi.sifre)

        # Veritabanına şifrenin kendisini DEĞİL, sadece hash'ini yazıyoruz:
        yeni_kullanici = Kullanici(
            email=kullanici_verisi.email,
            hashed_sifre=guvenli_sifre,
        )
        session.add(yeni_kullanici)
        session.commit()
        session.refresh(yeni_kullanici)

        # KullaniciPublic sayesinde dışarıya asla şifre veya hash sızmaz!
        return yeni_kullanici


# ==========================================
# KATEGORİ UÇ NOKTALARI (ENDPOINTS)
# ==========================================


# 2. YENİ KATEGORİ EKLEME (POST)
@app.post("/kategoriler", response_model=Kategori)
def kategori_ekle(kategori_verisi: KategoriCreate):
    with Session(engine) as session:
        db_kategori = Kategori.model_validate(kategori_verisi)
        session.add(db_kategori)
        session.commit()
        session.refresh(db_kategori)
        return db_kategori


# 3. TÜM KATEGORİLERİ LİSTELEME (GET)
@app.get("/kategoriler", response_model=list[Kategori])
def tum_kategorileri_getir():
    with Session(engine) as session:
        return session.exec(select(Kategori)).all()


# 4. OOP İLİŞKİ TESTİ: Bir kategorinin altındaki tüm ürünleri getirme!
@app.get("/kategoriler/{kategori_id}/urunler", response_model=list[Urun])
def kategorinin_urunlerini_getir(kategori_id: int):
    with Session(engine) as session:
        kategori = session.get(Kategori, kategori_id)
        if not kategori:
            raise HTTPException(status_code=404, detail="Kategori bulunamadı!")
        return kategori.urunler


# ==========================================
# ÜRÜN UÇ NOKTALARI (ENDPOINTS)
# ==========================================


# 5. YENİ ÜRÜN EKLEME (POST)
@app.post("/urunler", response_model=Urun)
def urun_ekle(urun_verisi: UrunCreate):
    with Session(engine) as session:
        if urun_verisi.kategori_id is not None:
            kategori = session.get(Kategori, urun_verisi.kategori_id)
            if not kategori:
                raise HTTPException(status_code=400, detail="Belirtilen kategori_id bulunamadı!")

        db_urun = Urun.model_validate(urun_verisi)
        session.add(db_urun)
        session.commit()
        session.refresh(db_urun)
        return db_urun


# 6. TÜM ÜRÜNLERİ LİSTELEME (GET)
@app.get("/urunler", response_model=list[Urun])
def tum_urunleri_getir():
    with Session(engine) as session:
        return session.exec(select(Urun)).all()


# 7. ID İLE ÜRÜN BULMA (GET)
@app.get("/urunler/{urun_id}", response_model=Urun)
def id_ile_urun_bul(urun_id: int):
    with Session(engine) as session:
        urun = session.get(Urun, urun_id)
        if not urun:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı!")
        return urun


# 8. OOP METODU TESTİ: KDV Hesaplama
@app.get("/urunler/{urun_id}/kdv")
def urun_kdv_hesapla(urun_id: int):
    with Session(engine) as session:
        urun = session.get(Urun, urun_id)
        if not urun:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı!")
        return {
            "urun": urun.isim,
            "net_fiyat": urun.fiyat,
            "kdv_dahil_fiyat": urun.kdv_dahil_fiyat(),
        }


# 9. ÜRÜN GÜNCELLEME (PATCH)
@app.patch("/urunler/{urun_id}", response_model=Urun)
def urun_guncelle(urun_id: int, urun_verisi: UrunUpdate):
    with Session(engine) as session:
        db_urun = session.get(Urun, urun_id)
        if not db_urun:
            raise HTTPException(status_code=404, detail="Güncellenecek ürün bulunamadı!")

        guncellenecekler = urun_verisi.model_dump(exclude_unset=True)
        db_urun.sqlmodel_update(guncellenecekler)

        session.add(db_urun)
        session.commit()
        session.refresh(db_urun)
        return db_urun


# 10. ÜRÜN SİLME (DELETE)
@app.delete("/urunler/{urun_id}")
def urun_sil(urun_id: int):
    with Session(engine) as session:
        urun = session.get(Urun, urun_id)
        if not urun:
            raise HTTPException(status_code=404, detail="Silinecek ürün bulunamadı!")
        session.delete(urun)
        session.commit()
        return {"mesaj": f"{urun_id} ID'li ürün veritabanından silindi!"}
