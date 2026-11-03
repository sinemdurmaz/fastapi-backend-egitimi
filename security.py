from datetime import datetime, timedelta, timezone
import jwt
from pwdlib import PasswordHash

# Modern ve en güvenli endüstri standardı (Argon2)
password_hash = PasswordHash.recommended()

# JWT Ayarları
# Gerçek projelerde bu anahtar .env dosyasında saklanır
SECRET_KEY = "super_gizli_ve_guvenli_backend_jwt_anahtari_2026_en_az_32_byte"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60


def sifre_hashle(sifre: str) -> str:
    return password_hash.hash(sifre)


def sifre_dogrula(duz_sifre: str, hashlenmis_sifre: str) -> bool:
    return password_hash.verify(duz_sifre, hashlenmis_sifre)


def token_olustur(veri: dict, gecerlilik_dakikasi: int = ACCESS_TOKEN_EXPIRE_MINUTES) -> str:
    kodlanacak_veri = veri.copy()
    bitis_zamani = datetime.now(timezone.utc) + timedelta(minutes=gecerlilik_dakikasi)
    kodlanacak_veri.update({"exp": bitis_zamani})
    return jwt.encode(kodlanacak_veri, SECRET_KEY, algorithm=ALGORITHM)
