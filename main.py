from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from sqlmodel import Session, select

from database import engine, veritabanini_olustur
from models import Kategori, KategoriCreate, Urun, UrunCreate, UrunUpdate


@asynccontextmanager
async def omur_dongusu(app: FastAPI):
    veritabanini_olustur()
    yield


app = FastAPI(title="OOP & İlişkili Veritabanlı Ürün API'si", lifespan=omur_dongusu)


# ==========================================
# KATEGORİ UÇ NOKTALARI (ENDPOINTS)
# ==========================================


# 1. YENİ KATEGORİ EKLEME (POST)
@app.post("/kategoriler", response_model=Kategori)
def kategori_ekle(kategori_verisi: KategoriCreate):
    with Session(engine) as session:
        db_kategori = Kategori.model_validate(kategori_verisi)
        session.add(db_kategori)
        session.commit()
        session.refresh(db_kategori)
        return db_kategori


# 2. TÜM KATEGORİLERİ LİSTELEME (GET)
@app.get("/kategoriler", response_model=list[Kategori])
def tum_kategorileri_getir():
    with Session(engine) as session:
        return session.exec(select(Kategori)).all()


# 3. OOP İLİŞKİ TESTİ: Bir kategorinin altındaki tüm ürünleri getirme!
@app.get("/kategoriler/{kategori_id}/urunler", response_model=list[Urun])
def kategorinin_urunlerini_getir(kategori_id: int):
    with Session(engine) as session:
        kategori = session.get(Kategori, kategori_id)
        if not kategori:
            raise HTTPException(status_code=404, detail="Kategori bulunamadı!")
        # OOP'nin gücü: SQL yazmadan doğrudan nesne üzerinden ürünlere eriştik!
        return kategori.urunler


# ==========================================
# ÜRÜN UÇ NOKTALARI (ENDPOINTS)
# ==========================================


# 4. YENİ ÜRÜN EKLEME (POST - kategori_id alabilir)
@app.post("/urunler", response_model=Urun)
def urun_ekle(urun_verisi: UrunCreate):
    with Session(engine) as session:
        # Eğer kategori_id verilmişse veritabanında var mı kontrol edelim
        if urun_verisi.kategori_id is not None:
            kategori = session.get(Kategori, urun_verisi.kategori_id)
            if not kategori:
                raise HTTPException(status_code=400, detail="Belirtilen kategori_id veritabanında bulunamadı!")

        db_urun = Urun.model_validate(urun_verisi)
        session.add(db_urun)
        session.commit()
        session.refresh(db_urun)
        return db_urun


# 5. TÜM ÜRÜNLERİ LİSTELEME (GET)
@app.get("/urunler", response_model=list[Urun])
def tum_urunleri_getir():
    with Session(engine) as session:
        return session.exec(select(Urun)).all()


# 6. ID İLE ÜRÜN BULMA (GET)
@app.get("/urunler/{urun_id}", response_model=Urun)
def id_ile_urun_bul(urun_id: int):
    with Session(engine) as session:
        urun = session.get(Urun, urun_id)
        if not urun:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı!")
        return urun


# 7. OOP METODU TESTİ: KDV Hesaplama
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


# 8. ÜRÜN GÜNCELLEME (PATCH)
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


# 9. ÜRÜN SİLME (DELETE)
@app.delete("/urunler/{urun_id}")
def urun_sil(urun_id: int):
    with Session(engine) as session:
        urun = session.get(Urun, urun_id)
        if not urun:
            raise HTTPException(status_code=404, detail="Silinecek ürün bulunamadı!")
        session.delete(urun)
        session.commit()
        return {"mesaj": f"{urun_id} ID'li ürün veritabanından silindi!"}
