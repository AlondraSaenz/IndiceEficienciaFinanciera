import pandas as pd
import pyodbc
import random

positivos = [
    "Excelente atención y muy buenos médicos.",
    "Muy agradecida con el personal, muy amables.",
    "El servicio fue rápido y eficiente.",
    "La clínica está impecable y segura.",
    "¡Felicitaciones por el gran trabajo!",
    "Volvería sin dudarlo, me encantó.",
    "Todo el equipo fue muy atento.",
    "Me sentí cuidada en todo momento.",
    "Muy profesional y humano el trato.",
    "Recomiendo la clínica a todos."
]

negativos = [
    "No me atendieron a tiempo, muy demorado.",
    "El precio es demasiado alto para la calidad.",
    "Muy mala experiencia, no regreso.",
    "Me hicieron esperar más de una hora.",
    "No recomiendo la clínica, mal servicio.",
    "Me sentí ignorado por el personal.",
    "La atención al cliente es pésima.",
    "El doctor fue muy descortés.",
    "Instalaciones descuidadas y sucias.",
    "Faltó empatía en todo momento."
]

neutrales = [
    "La consulta fue normal, nada especial.",
    "Todo estuvo bien, sin destacar.",
    "Servicio promedio, como cualquier otro.",
    "Cumplieron con lo mínimo necesario.",
    "Nada que destacar, ni bueno ni malo."
]

comentarios_base = positivos * 10 + negativos * 10 + neutrales * 4
random.shuffle(comentarios_base)
comentarios = comentarios_base[:200]

df = pd.DataFrame(comentarios, columns=['Comentario'])
excel_path = "ComentariosClinicaSanna_200.xlsx"
df.to_excel(excel_path, index=False)
print(f"Archivo Excel generado: {excel_path}")

server = 'DESKTOP-DHTBPN6\\SQLSERVER2022'
database_clinica = 'ClinicaSanna'
database_indice = 'INDICE_DE_EFICIENCIA_FINANCIERA'
username = 'Eficiencia'
password = '1234'
driver = '{ODBC Driver 17 for SQL Server}'

conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database_clinica};UID={username};PWD={password}'
create_table_sql = """
IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ComentariosInstagram' AND xtype='U')
BEGIN
    CREATE TABLE ComentariosInstagram (
        ComentarioID INT IDENTITY(1,1) PRIMARY KEY,
        Comentario NVARCHAR(500),
        Polaridad FLOAT,
        Sentimiento NVARCHAR(20),
        FechaRegistro DATETIME DEFAULT GETDATE()
    )
END
"""
try:
 
    conn = pyodbc.connect(conn_str)
    cursor = conn.cursor()
    cursor.execute(create_table_sql)
    conn.commit()
    print("Tabla ComentariosInstagram verificada / creada en ClinicaSanna.")

    positivos_count = 0
    negativos_count = 0
    neutrales_count = 0

    for comentario in comentarios:
        if comentario in positivos:
            polaridad = random.uniform(0.3, 1.0)
            sentimiento = "Positivo"
            positivos_count += 1
        elif comentario in negativos:
            polaridad = random.uniform(-1.0, -0.3)
            sentimiento = "Negativo"
            negativos_count += 1
        else:
            polaridad = random.uniform(-0.1, 0.1)
            sentimiento = "Neutral"
            neutrales_count += 1

        cursor.execute("""
            INSERT INTO ComentariosInstagram (Comentario, Polaridad, Sentimiento)
            VALUES (?, ?, ?)
        """, comentario, polaridad, sentimiento)

    conn.commit()
    print("Comentarios insertados y analizados en ClinicaSanna.")


    conn_destino_str = f'DRIVER={driver};SERVER={server};DATABASE={database_indice};UID={username};PWD={password}'
    conn_destino = pyodbc.connect(conn_destino_str)
    cursor_destino = conn_destino.cursor()

   
    create_dim_sql = """
    IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='ComentarioInstagram_Dim' AND xtype='U')
    BEGIN
        CREATE TABLE ComentarioInstagram_Dim (
            id_comentario INT PRIMARY KEY,
            comentario NVARCHAR(500),
            polaridad FLOAT,
            sentimiento NVARCHAR(20),
            fecha_registro DATETIME
        )
    END
    """
    cursor_destino.execute(create_dim_sql)
    conn_destino.commit()
    print("Tabla ComentarioInstagram_Dim verificada / creada en INDICE_DE_EFICIENCIA_FINANCIERA.")


    cursor.execute("SELECT ComentarioID, Comentario, Polaridad, Sentimiento, FechaRegistro FROM ComentariosInstagram")
    rows = cursor.fetchall()

   
    for row in rows:
        cursor_destino.execute("""
            INSERT INTO ComentarioInstagram_Dim (id_comentario, comentario, polaridad, sentimiento, fecha_registro)
            VALUES (?, ?, ?, ?, ?)
        """, row.ComentarioID, row.Comentario, row.Polaridad, row.Sentimiento, row.FechaRegistro)

    conn_destino.commit()
    print("Migración completada a INDICE_DE_EFICIENCIA_FINANCIERA.")

  
    total = positivos_count + negativos_count + neutrales_count
    print("\nResumen de sentimientos:")
    print(f"Positivos: {positivos_count} ({positivos_count / total * 100:.1f}%)")
    print(f"Negativos: {negativos_count} ({negativos_count / total * 100:.1f}%)")
    print(f"Neutrales: {neutrales_count} ({neutrales_count / total * 100:.1f}%)")

    if positivos_count > negativos_count:
        print("\nConclusión: En general, la percepción es positiva. Los pacientes valoran la atención y la calidad humana.")
    elif negativos_count > positivos_count:
        print("\nConclusión: Predominan los comentarios negativos, se recomienda trabajar en la atención y tiempos de espera.")
    else:
        print("\nConclusión: Hay opiniones mixtas, se debe reforzar la experiencia positiva y corregir puntos críticos.")

except Exception as e:
    print("Error general:", e)

finally:
    if conn:
        conn.close()
    if 'conn_destino' in locals():
        conn_destino.close()