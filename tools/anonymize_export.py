#!/usr/bin/env python3
"""
tools/anonymize_export.py

Esqueleto de script para generar exportes anonimizados desde la DB.
- Conecta a la DB (psycopg2 / asyncpg)
- Extrae tablas necesarias
- Aplica transformaciones: drop PII, bucket dates, hash con salt
- Guarda CSV/JSON listos para subir al repositorio público con README
"""

import csv
import hashlib
import json
import os
from datetime import datetime
from typing import Dict

# CONFIG: cambiar según entorno
SALT = os.environ.get("ANON_SALT", "cambiami_ya")
OUTPUT_DIR = "exports/anon"

def hash_value(value: str, salt: str = SALT) -> str:
    if value is None:
        return ""
    return hashlib.sha256((salt + value).encode("utf-8")).hexdigest()

def bucket_year(date_str: str) -> int:
    try:
        dt = datetime.fromisoformat(date_str)
        return dt.year
    except Exception:
        return None

def anonymize_row(row: Dict, fields_to_hash: list, date_fields: list):
    out = dict(row)
    for f in fields_to_hash:
        if f in out:
            out[f] = hash_value(str(out[f]))
    for d in date_fields:
        if d in out:
            out[d] = bucket_year(out[d])  # ejemplo: reemplazar por año
    # Eliminar campos sensibles adicionales
    for sensitive in ["email", "name", "phone", "address"]:
        if sensitive in out:
            out.pop(sensitive, None)
    return out

def main():
    # Este es un esqueleto: conectar a la DB y extraer los datos reales
    # Luego aplicar anonymize_row a cada registro y guardar CSV/JSON
    sample = [
        {"id": "1", "pseudonym": "user1", "email": "user1@example.com", "created_at": "2024-06-01T12:00:00Z", "phq9": 12}
    ]
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out_rows = []
    for r in sample:
        out_rows.append(anonymize_row(r, fields_to_hash=["pseudonym"], date_fields=["created_at"]))
    out_path = os.path.join(OUTPUT_DIR, "assessments_anon.json")
    with open(out_path, "w", encoding="utf-8") as fh:
        json.dump(out_rows, fh, ensure_ascii=False, indent=2)
    print(f"Export generado en {out_path}")

if __name__ == "__main__":
    main()
