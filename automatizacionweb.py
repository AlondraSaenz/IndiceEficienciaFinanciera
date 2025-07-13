import pandas as pd
import pyodbc
from collections import Counter
import re

comentarios_web = [
    "Muy buen servicio online, rápido y claro.",
    "Me costó mucho encontrar la información en la web.",
    "El chatbot fue muy útil para resolver mis dudas.",
    "No encontré los precios en la página, debería ser más transparente.",
    "Excelente diseño y muy intuitivo.",
    "La web carga lento en mi celular.",
    "Buena experiencia navegando desde la laptop.",
    "Demasiada publicidad en la página.",
    "Me encantó el formulario de citas, muy fácil.",
    "No pude terminar el pago en línea, un desastre.",
    "Todo muy rápido y seguro, me gustó.",
    "Poca información de médicos disponibles.",
    "Fácil encontrar especialidades.",
    "Recomiendo mucho la web de la clínica.",
    "Tardan en responder por el chat online.",
    "Información completa y detallada.",
    "Demasiados pasos para agendar una cita.",
    "Muy útil la opción para descargar exámenes.",
    "Pocos métodos de pago aceptados.",
    "Fácil de usar, volvería a usarla sin problema."
]

df = pd.DataFrame(comentarios_web, columns=['Comentario'])


excel_path = "ComentariosWeb.xlsx"
df.to_excel(excel_path, index=False)
print(f"Archivo Excel generado: {excel_path}")


all_words = []

for comentario in comentarios_web:
    comentario_limpio = re.sub(r'[^\w\s]', '', comentario.lower())
    palabras = comentario_limpio.split()
    all_words.extend(palabras)

contador = Counter(all_words)
palabras_comunes = contador.most_common(20)

df_palabras = pd.DataFrame(palabras_comunes, columns=['Palabra', 'Frecuencia'])


excel_palabras_path = "ResumenPalabrasWeb.xlsx"
df_palabras.to_excel(excel_palabras_path, index=False)
print(f"Archivo Excel de palabras generado: {excel_palabras_path}")


temas_positivos = ["rapido", "util", "excelente", "facil", "seguro", "intuitivo", "recomiendo"]
temas_negativos = ["lento", "publicidad", "poco", "desastre", "difícil", "problema", "demasiados"]

conclusion = "Los comentarios web son variados, sin tendencia clara."

if any(word in contador for word in temas_positivos):
    conclusion = "Predominan comentarios positivos sobre la facilidad y utilidad de la web."
elif any(word in contador for word in temas_negativos):
    conclusion = "Destacan críticas a la lentitud y problemas para terminar procesos online."

print("\nConclusión Web:", conclusion)


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

    
    cursor.execute("IF OBJECT_ID('ResumenPalabrasWeb', 'U') IS NOT NULL DELETE FROM ResumenPalabrasWeb;")
    cursor.execute("IF OBJECT_ID('AnalisisWebConclusion', 'U') IS NOT NULL DELETE FROM AnalisisWebConclusion;")
    conn.commit()
    print("Tablas web limpiadas en ClinicaSanna.")

  
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ResumenPalabrasWeb' AND xtype='U')
    BEGIN
        CREATE TABLE ResumenPalabrasWeb (
            PalabraID INT IDENTITY(1,1) PRIMARY KEY,
            Palabra NVARCHAR(100),
            Frecuencia INT,
            FechaRegistro DATETIME DEFAULT GETDATE()
        )
    END
    """)
    cursor.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='AnalisisWebConclusion' AND xtype='U')
    BEGIN
        CREATE TABLE AnalisisWebConclusion (
            ConclusionID INT IDENTITY(1,1) PRIMARY KEY,
            Texto NVARCHAR(1000),
            FechaRegistro DATETIME DEFAULT GETDATE()
        )
    END
    """)
    conn.commit()
    print("Tablas web creadas/verificadas en ClinicaSanna.")


    for palabra, freq in palabras_comunes:
        cursor.execute("""
            INSERT INTO ResumenPalabrasWeb (Palabra, Frecuencia)
            VALUES (?, ?)
        """, palabra, freq)

  
    cursor.execute("""
        INSERT INTO AnalisisWebConclusion (Texto)
        VALUES (?)
    """, conclusion)

    conn.commit()
    print("Datos insertados en ClinicaSanna (web).")


    conn_destino = pyodbc.connect(conn_destino_str)
    cursor_destino = conn_destino.cursor()

   
    cursor_destino.execute("IF OBJECT_ID('ResumenPalabrasWeb_Dim', 'U') IS NOT NULL DELETE FROM ResumenPalabrasWeb_Dim;")
    cursor_destino.execute("IF OBJECT_ID('AnalisisWebConclusion_Dim', 'U') IS NOT NULL DELETE FROM AnalisisWebConclusion_Dim;")
    conn_destino.commit()
    print("Tablas web limpiadas en INDICE_DE_EFICIENCIA_FINANCIERA.")

   
    cursor_destino.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ResumenPalabrasWeb_Dim' AND xtype='U')
    BEGIN
        CREATE TABLE ResumenPalabrasWeb_Dim (
            id_palabra INT PRIMARY KEY,
            palabra NVARCHAR(100),
            frecuencia INT,
            fecha_registro DATETIME
        )
    END
    """)
    cursor_destino.execute("""
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='AnalisisWebConclusion_Dim' AND xtype='U')
    BEGIN
        CREATE TABLE AnalisisWebConclusion_Dim (
            id_conclusion INT PRIMARY KEY,
            texto NVARCHAR(1000),
            fecha_registro DATETIME
        )
    END
    """)
    conn_destino.commit()
    print("Tablas web creadas/verificadas en INDICE_DE_EFICIENCIA_FINANCIERA.")

    
    cursor.execute("SELECT PalabraID, Palabra, Frecuencia, FechaRegistro FROM ResumenPalabrasWeb")
    rows_palabras = cursor.fetchall()

    for row in rows_palabras:
        cursor_destino.execute("""
            INSERT INTO ResumenPalabrasWeb_Dim (id_palabra, palabra, frecuencia, fecha_registro)
            VALUES (?, ?, ?, ?)
        """, row.PalabraID, row.Palabra, row.Frecuencia, row.FechaRegistro)

   
    cursor.execute("SELECT ConclusionID, Texto, FechaRegistro FROM AnalisisWebConclusion")
    rows_conclusion = cursor.fetchall()

    for row in rows_conclusion:
        cursor_destino.execute("""
            INSERT INTO AnalisisWebConclusion_Dim (id_conclusion, texto, fecha_registro)
            VALUES (?, ?, ?)
        """, row.ConclusionID, row.Texto, row.FechaRegistro)

    conn_destino.commit()
    print("Migración completada a INDICE_DE_EFICIENCIA_FINANCIERA (web).")

except Exception as e:
    print("Error general:", e)

finally:
    if 'conn' in locals():
        conn.close()
    if 'conn_destino' in locals():
        conn_destino.close()
