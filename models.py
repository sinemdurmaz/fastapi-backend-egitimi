from sqlmodel import Field, SQLModel


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


# 4. GÜNCELLEME İÇİN VERİ KALIBI (Tüm alanlar opsiyonel)
class UrunUpdate(SQLModel):
    isim: str | None = None
    fiyat: int | None = None
    stokta_var_mi: bool | None = None
