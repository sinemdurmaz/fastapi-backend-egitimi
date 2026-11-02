from sqlmodel import SQLModel, create_engine

sqlite_dosyasi = "veritabani.db"
sqlite_url = f"sqlite:///{sqlite_dosyasi}"
# echo=True ile SQL sorgularını terminalde görebiliriz
engine = create_engine(sqlite_url, echo=True)


def veritabanini_olustur():
    SQLModel.metadata.create_all(engine)
