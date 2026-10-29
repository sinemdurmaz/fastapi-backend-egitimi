from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from sqlmodel import Field, Session, SQLModel, create_engine, select


# 1. ORTAK ATA MODEL (Base Class)
class UrunBase(SQLModel):
    isim: str
    fiyat: int
    stokta_var_mi: bool = True

    # OOP Metodu: Nesnenin kendi verisiyle (self.fiyat) KDV hesaplaması
    def kdv_dahil_fiyat(self) -> float:
        return round(self.fiyat * 1.20, 2)


# 2. KULLANICIDAN VERİ ALIRKEN (ID Yok - Miras Alır)
class UrunCreate(UrunBase):
    pass


# 3. VERİTABANI TABLOSU (ID Var - Miras Alır)
class Urun(UrunBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


# Veritabanı Bağlantısı ve Motoru
sqlite_dosyasi = "veritabani.db"
sqlite_url = f"sqlite:///{sqlite_dosyasi}"
engine = create_engine(sqlite_url, echo=True)


@asynccontextmanager
async def omur_dongusu(app: FastAPI):
    SQLModel.metadata.create_all(engine)
    yield


app = FastAPI(title="OOP Destekli Veritabanlı Ürün API'si", lifespan=omur_dongusu)


# YENİ ÜRÜN EKLEME (POST - UrunCreate sayesinde kullanıcıdan ID istemez!)
@app.post("/urunler", response_model=Urun)
def urun_ekle(urun_verisi: UrunCreate):
    with Session(engine) as session:
        # Gelen veriyi veritabanı modeline dönüştürüyoruz
        db_urun = Urun.model_validate(urun_verisi)
        session.add(db_urun)
        session.commit()
        session.refresh(db_urun)
        return db_urun


# TÜM ÜRÜNLERİ LİSTELEME (GET)
@app.get("/urunler", response_model=list[Urun])
def tum_urunleri_getir():
    with Session(engine) as session:
        return session.exec(select(Urun)).all()


# ID İLE ÜRÜN BULMA (GET)
@app.get("/urunler/{urun_id}", response_model=Urun)
def id_ile_urun_bul(urun_id: int):
    with Session(engine) as session:
        urun = session.get(Urun, urun_id)
        if not urun:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı!")
        return urun


# OOP METODU TESTİ: KDV Hesaplama (Nesne kendi metodunu çağırır)
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


# ÜRÜN SİLME (DELETE)
@app.delete("/urunler/{urun_id}")
def urun_sil(urun_id: int):
    with Session(engine) as session:
        urun = session.get(Urun, urun_id)
        if not urun:
            raise HTTPException(status_code=404, detail="Silinecek ürün bulunamadı!")
        session.delete(urun)
        session.commit()
        return {"mesaj": f"{urun_id} ID'li ürün veritabanından silindi!"}
