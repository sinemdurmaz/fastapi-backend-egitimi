from sqlmodel import Field, Relationship, SQLModel


# ==========================================
# 1. KATEGORİ MODELLERİ
# ==========================================
class KategoriBase(SQLModel):
    ad: str


class KategoriCreate(KategoriBase):
    pass


class Kategori(KategoriBase, table=True):
    id: int | None = Field(default=None, primary_key=True)

    # OOP İlişkisi: Bu kategoriye ait ürünler
    urunler: list["Urun"] = Relationship(back_populates="kategori")


# ==========================================
# 2. KULLANICI MODELLERİ (AUTH)
# ==========================================
class KullaniciBase(SQLModel):
    email: str = Field(unique=True, index=True)


class KullaniciCreate(KullaniciBase):
    sifre: str


class Kullanici(KullaniciBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_sifre: str

    # OOP İlişkisi: Bu kullanıcının eklediği ürünler
    urunler: list["Urun"] = Relationship(back_populates="sahip")


class KullaniciPublic(KullaniciBase):
    id: int


# ==========================================
# 3. ÜRÜN MODELLERİ
# ==========================================
class UrunBase(SQLModel):
    isim: str
    fiyat: int
    stokta_var_mi: bool = True
    kategori_id: int | None = Field(default=None, foreign_key="kategori.id")

    # OOP Metodu: Nesnenin kendi verisiyle (self.fiyat) KDV hesaplaması
    def kdv_dahil_fiyat(self) -> float:
        return round(self.fiyat * 1.20, 2)


class UrunCreate(UrunBase):
    pass


class Urun(UrunBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    # Ürünü hangi kullanıcının eklediğini tutan yabancı anahtar (Foreign Key):
    sahip_id: int | None = Field(default=None, foreign_key="kullanici.id")

    # OOP İlişkileri: Doğrudan Kategori ve Kullanici nesnelerini tanır
    kategori: Kategori | None = Relationship(back_populates="urunler")
    sahip: Kullanici | None = Relationship(back_populates="urunler")


class UrunUpdate(SQLModel):
    isim: str | None = None
    fiyat: int | None = None
    stokta_var_mi: bool | None = None
    kategori_id: int | None = None


# ==========================================
# 4. JWT TOKEN MODELİ
# ==========================================
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
