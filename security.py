from pwdlib import PasswordHash

# Modern ve en güvenli endüstri standardı (Argon2)
password_hash = PasswordHash.recommended()


def sifre_hashle(sifre: str) -> str:
    return password_hash.hash(sifre)


def sifre_dogrula(duz_sifre: str, hashlenmis_sifre: str) -> bool:
    return password_hash.verify(duz_sifre, hashlenmis_sifre)
