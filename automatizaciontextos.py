import pandas as pd
import pyodbc
from collections import Counter
import re

df = pd.read_excel("ComentariosClinicaSanna_200.xlsx")
comentarios = df['Comentario'].tolist()

all_words = []

for comentario in comentarios:
    comentario_limpio = re.sub(r'[^\w\s]', '', comentario.lower())
    palabras = comentario_limpio.split()
    all_words.extend(palabras)

contador = Counter(all_words)
palabras_comunes = contador.most_common(30)


df_palabras = pd.DataFrame(palabras_comunes, columns=['Palabra', 'Frecuencia'])


excel_path = "ResumenPalabras.xlsx"
df_palabras.to_excel(excel_path, index=False)
print(f"Archivo Excel generado: {excel_path}")


temas_positivos = ["atencion", "amables", "rapido", "segura", "profesional", "recomiendo"]
temas_negativos = ["espera", "precio", "mala", "demorado", "descortes"]

conclusion = "Los comentarios son variados, sin un tema dominante."

if any(word in contador for word in temas_positivos):
    conclusion = "Predominan aspectos positivos, especialmente la buena atención y profesionalismo."
elif any(word in contador for word in temas_negativos):
    conclusion = "Se destacan aspectos negativos como demoras y quejas sobre el precio."

print("\nConclusión:", conclusion)

server = 'DESKTOP-DHTBPN6\\SQLSERVER2022'
database_clinica = 'ClinicaSanna'
database_indice = 'INDICE_DE_EFICIENCIA_FINANCIERA'
username = 'Eficiencia'
password = '1234'
driver = '{ODBC Driver 17 for SQL Server}'

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database_clinica};UID={username};PWD={password}'
conn_destino_str = f'DRIVER={driver};SERVER={server};DATABASE={database_indice};UID={username};PWD={password}'

try:
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()

 
    cursor.execute("DELETE FROM ResumenPalabras;")
    cursor.execute("DELETE FROM AnalisisTextoConclusion;")
    conn.commit()
    print("Tablas limpiadas en ClinicaSanna.")

    
    cursor.execute("""
        IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'ResumenPalabras' AND COLUMN_NAME = 'Palabra' AND CHARACTER_MAXIMUM_LENGTH = 1)
        BEGIN
            ALTER TABLE ResumenPalabras ALTER COLUMN Palabra NVARCHAR(100)
        END
    """)
    cursor.execute("""
        IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'AnalisisTextoConclusion' AND COLUMN_NAME = 'Texto' AND CHARACTER_MAXIMUM_LENGTH = 1)
        BEGIN
            ALTER TABLE AnalisisTextoConclusion ALTER COLUMN Texto NVARCHAR(1000)
        END
    """)
    conn.commit()
    print("Columnas corregidas en ClinicaSanna.")

    
    for palabra, freq in palabras_comunes:
        cursor.execute("""
            INSERT INTO ResumenPalabras (Palabra, Frecuencia)
            VALUES (?, ?)
        """, palabra, freq)

   
    cursor.execute("""
        INSERT INTO AnalisisTextoConclusion (Texto)
        VALUES (?)
    """, conclusion)

    conn.commit()
    print("Datos insertados en ClinicaSanna.")

    conn_destino = pyodbc.connect(conn_destino_str)
    cursor_destino = conn_destino.cursor()

   
    cursor_destino.execute("DELETE FROM ResumenPalabras_Dim;")
    cursor_destino.execute("DELETE FROM AnalisisTextoConclusion_Dim;")
    conn_destino.commit()
    print("Tablas limpiadas en INDICE_DE_EFICIENCIA_FINANCIERA.")


    cursor_destino.execute("""
        IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'ResumenPalabras_Dim' AND COLUMN_NAME = 'palabra' AND CHARACTER_MAXIMUM_LENGTH = 1)
        BEGIN
            ALTER TABLE ResumenPalabras_Dim ALTER COLUMN palabra NVARCHAR(100)
        END
    """)
    cursor_destino.execute("""
        IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = 'AnalisisTextoConclusion_Dim' AND COLUMN_NAME = 'texto' AND CHARACTER_MAXIMUM_LENGTH = 1)
        BEGIN
            ALTER TABLE AnalisisTextoConclusion_Dim ALTER COLUMN texto NVARCHAR(1000)
        END
    """)
    conn_destino.commit()
    print("Columnas corregidas en INDICE_DE_EFICIENCIA_FINANCIERA.")

 
    cursor.execute("SELECT PalabraID, Palabra, Frecuencia, FechaRegistro FROM ResumenPalabras")
    rows_palabras = cursor.fetchall()

    for row in rows_palabras:
        cursor_destino.execute("""
            INSERT INTO ResumenPalabras_Dim (id_palabra, palabra, frecuencia, fecha_registro)
            VALUES (?, ?, ?, ?)
        """, row.PalabraID, row.Palabra, row.Frecuencia, row.FechaRegistro)

    cursor.execute("SELECT ConclusionID, Texto, FechaRegistro FROM AnalisisTextoConclusion")
    rows_conclusion = cursor.fetchall()

    for row in rows_conclusion:
        cursor_destino.execute("""
            INSERT INTO AnalisisTextoConclusion_Dim (id_conclusion, texto, fecha_registro)
            VALUES (?, ?, ?)
        """, row.ConclusionID, row.Texto, row.FechaRegistro)

    conn_destino.commit()
    print("Migración completada a INDICE_DE_EFICIENCIA_FINANCIERA.")

except Exception as e:
    print("Error general:", e)

finally:
    if 'conn' in locals():
        conn.close()
    if 'conn_destino' in locals():
        conn_destino.close()
