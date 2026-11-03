from contextlib import asynccontextmanager
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, select

from database import engine, veritabanini_olustur
from models import (
    Kategori,
    KategoriCreate,
    Kullanici,
    KullaniciCreate,
    KullaniciPublic,
    Token,
    Urun,
    UrunCreate,
    UrunUpdate,
)
from security import (
    oauth2_scheme,
    sifre_dogrula,
    sifre_hashle,
    token_coz,
    token_olustur,
)


@asynccontextmanager
async def omur_dongusu(app: FastAPI):
    veritabanini_olustur()
    yield


app = FastAPI(title="OOP, Auth & Güvenlik Destekli API", lifespan=omur_dongusu)


# =======================================================
# GÜVENLİK BEKÇİSİ (DEPENDENCY INJECTION - DEPENDS)
# =======================================================
def giris_yapmis_kullaniciyi_al(token: str = Depends(oauth2_scheme)) -> Kullanici:
    payload = token_coz(token)
    if not payload or "sub" not in payload:
        raise HTTPException(
            status_code=401,
            detail="Geçersiz veya süresi dolmuş oturum bileti (Token)!",
            headers={"WWW-Authenticate": "Bearer"},
        )

    with Session(engine) as session:
        kullanici = session.exec(
            select(Kullanici).where(Kullanici.email == payload["sub"])
        ).first()
        if not kullanici:
            raise HTTPException(
                status_code=401,
                detail="Kullanıcı bulunamadı!",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return kullanici


# ==========================================
# KİMLİK DOĞRULAMA (AUTH) UÇ NOKTALARI
# ==========================================


# 1. YENİ KULLANICI KAYDI (REGISTER)
@app.post("/auth/kayit", response_model=KullaniciPublic)
def kullanici_kayit(kullanici_verisi: KullaniciCreate):
    with Session(engine) as session:
        mevcut_kullanici = session.exec(
            select(Kullanici).where(Kullanici.email == kullanici_verisi.email)
        ).first()
        if mevcut_kullanici:
            raise HTTPException(status_code=400, detail="Bu e-posta adresi zaten kullanımda!")

        guvenli_sifre = sifre_hashle(kullanici_verisi.sifre)
        yeni_kullanici = Kullanici(
            email=kullanici_verisi.email,
            hashed_sifre=guvenli_sifre,
        )
        session.add(yeni_kullanici)
        session.commit()
        session.refresh(yeni_kullanici)
        return yeni_kullanici


# 2. KULLANICI GİRİŞİ (LOGIN -> JWT BİLETİ DÖNER)
@app.post("/auth/giris", response_model=Token)
def kullanici_giris(giris_verisi: KullaniciCreate):
    with Session(engine) as session:
        kullanici = session.exec(
            select(Kullanici).where(Kullanici.email == giris_verisi.email)
        ).first()

        if not kullanici or not sifre_dogrula(giris_verisi.sifre, kullanici.hashed_sifre):
            raise HTTPException(
                status_code=401,
                detail="E-posta veya şifre hatalı!"
            )

        bilet = token_olustur(veri={"sub": kullanici.email, "id": kullanici.id})
        return {"access_token": bilet, "token_type": "bearer"}


# 3. KULLANICI PROFİLİ (KORUMALI ALAN TESTİ)
@app.get("/auth/profil", response_model=KullaniciPublic)
def kullanici_profil(kullanici: Kullanici = Depends(giris_yapmis_kullaniciyi_al)):
    # Buraya sadece geçerli token sahipleri girebilir
    return kullanici


# ==========================================
# KATEGORİ UÇ NOKTALARI (ENDPOINTS)
# ==========================================


# 4. YENİ KATEGORİ EKLEME (KORUMALI - Sadece giriş yapanlar ekleyebilir)
@app.post("/kategoriler", response_model=Kategori)
def kategori_ekle(
    kategori_verisi: KategoriCreate,
    kullanici: Kullanici = Depends(giris_yapmis_kullaniciyi_al),
):
    with Session(engine) as session:
        db_kategori = Kategori.model_validate(kategori_verisi)
        session.add(db_kategori)
        session.commit()
        session.refresh(db_kategori)
        return db_kategori


# 5. TÜM KATEGORİLERİ LİSTELEME (AÇIK - Herkes görebilir)
@app.get("/kategoriler", response_model=list[Kategori])
def tum_kategorileri_getir():
    with Session(engine) as session:
        return session.exec(select(Kategori)).all()


# 6. OOP İLİŞKİ TESTİ: Bir kategorinin altındaki tüm ürünleri getirme (AÇIK)
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


# 7. YENİ ÜRÜN EKLEME (KORUMALI - Sadece giriş yapanlar ekleyebilir)
@app.post("/urunler", response_model=Urun)
def urun_ekle(
    urun_verisi: UrunCreate,
    kullanici: Kullanici = Depends(giris_yapmis_kullaniciyi_al),
):
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


# 8. TÜM ÜRÜNLERİ LİSTELEME (AÇIK - Herkes görebilir)
@app.get("/urunler", response_model=list[Urun])
def tum_urunleri_getir():
    with Session(engine) as session:
        return session.exec(select(Urun)).all()


# 9. ID İLE ÜRÜN BULMA (AÇIK - Herkes görebilir)
@app.get("/urunler/{urun_id}", response_model=Urun)
def id_ile_urun_bul(urun_id: int):
    with Session(engine) as session:
        urun = session.get(Urun, urun_id)
        if not urun:
            raise HTTPException(status_code=404, detail="Ürün bulunamadı!")
        return urun


# 10. OOP METODU TESTİ: KDV Hesaplama (AÇIK)
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


# 11. ÜRÜN GÜNCELLEME (KORUMALI - Sadece giriş yapanlar güncelleyebilir)
@app.patch("/urunler/{urun_id}", response_model=Urun)
def urun_guncelle(
    urun_id: int,
    urun_verisi: UrunUpdate,
    kullanici: Kullanici = Depends(giris_yapmis_kullaniciyi_al),
):
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


# 12. ÜRÜN SİLME (KORUMALI - Sadece giriş yapanlar silebilir)
@app.delete("/urunler/{urun_id}")
def urun_sil(
    urun_id: int,
    kullanici: Kullanici = Depends(giris_yapmis_kullaniciyi_al),
):
    with Session(engine) as session:
        urun = session.get(Urun, urun_id)
        if not urun:
            raise HTTPException(status_code=404, detail="Silinecek ürün bulunamadı!")
        session.delete(urun)
        session.commit()
        return {"mesaj": f"{urun_id} ID'li ürün veritabanından silindi!"}
