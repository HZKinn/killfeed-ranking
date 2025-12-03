import re
import sqlite3
import os

PASTA = r"C:\Killfeed"  # pasta onde ficam os TXT exportados
DB = "ranking.db"

# REGEX (vou ajustar quando você me enviar uma linha real)
regex = re.compile(r"(.*?) apagou (.*?) - (.*?) - (\d+)m", re.IGNORECASE)

conn = sqlite3.connect(DB)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS kills (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    killer TEXT,
    victim TEXT,
    weapon TEXT,
    distance INT
)
""")

def processar_arquivo(txtfile):
    with open(txtfile, "r", encoding="utf8", errors="ignore") as f:
        for linha in f:
            m = regex.search(linha)
            if m:
                killer, victim, weapon, dist = m.groups()
                cur.execute(
                    "INSERT INTO kills (killer, victim, weapon, distance) VALUES (?, ?, ?, ?)",
                    (killer.strip(), victim.strip(), weapon.strip(), int(dist))
                )
                conn.commit()
                print("Novo kill:", killer, "→", victim)

print("Processando arquivos em:", PASTA)
for file in os.listdir(PASTA):
    if file.endswith(".txt"):
        processar_arquivo(os.path.join(PASTA, file))

print("Processamento concluído.")
