import hashlib
import hmac
import os
import secrets

ITERACIONES = 200_000  # más vueltas = más difícil de adivinar por fuerza bruta


def hashear(texto):
    """Convierte un texto en un 'hash' irreversible, con una sal aleatoria."""
    sal = os.urandom(16)
    hash_bytes = hashlib.pbkdf2_hmac(
        "sha256", texto.encode("utf-8"), sal, ITERACIONES
    )
    return f"pbkdf2${ITERACIONES}${sal.hex()}${hash_bytes.hex()}"


def verificar(texto, guardado):
    """Revisa si 'texto' corresponde al hash guardado."""
    try:
        _, iteraciones, sal, hash_hex = guardado.split("$")
        calculado = hashlib.pbkdf2_hmac(
            "sha256", texto.encode("utf-8"), bytes.fromhex(sal), int(iteraciones)
        )
        return hmac.compare_digest(calculado.hex(), hash_hex)
    except (ValueError, AttributeError):
        return False


def generar_token():
    """Texto aleatorio largo para identificar una sesión."""
    return secrets.token_hex(32)


def generar_codigo_recuperacion():
    """Código tipo ABCD-EFGH-JKLM (sin letras confusas como O, 0, I, 1)."""
    alfabeto = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"
    c = "".join(secrets.choice(alfabeto) for _ in range(12))
    return f"{c[:4]}-{c[4:8]}-{c[8:]}"


def normalizar_codigo(codigo):
    """Quita guiones y espacios y pasa a mayúsculas, para comparar bien."""
    return codigo.upper().replace("-", "").replace(" ", "")