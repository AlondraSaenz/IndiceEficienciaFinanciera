import os
import tarfile
import pyodbc
import pandas as pd
import datetime

# Configuración general
EXCEL_FILE = r'C:\Users\USUARIO\Downloads\Personas.xlsx'
ARCHIVO_TAR = r'C:\Users\USUARIO\Downloads\part1.tar.gz'
CARPETA_EXTRACCION = r'C:\Users\USUARIO\Downloads\imagenes_extraidas'

server = 'DESKTOP-DHTBPN6\\SQLSERVER2022'
user = 'Eficiencia'
password = '1234'
driver = '{ODBC Driver 17 for SQL Server}'

def conexion_sql(db):
    return pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={db};UID={user};PWD={password}'
    )

def extraer_fotos_renombradas():
    if not os.path.exists(CARPETA_EXTRACCION):
        os.makedirs(CARPETA_EXTRACCION)
    with tarfile.open(ARCHIVO_TAR, 'r:gz') as tar:
        tar.extractall(path=CARPETA_EXTRACCION)

    archivos = []
    for root, _, files in os.walk(CARPETA_EXTRACCION):
        for file in sorted(files):
            if file.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp')):
                archivos.append(os.path.join(root, file))

    for idx, path in enumerate(archivos, start=1):
        extension = os.path.splitext(path)[1].lower()
        nuevo_nombre = f'PER{str(idx).zfill(3)}{extension}'
        nuevo_path = os.path.join(CARPETA_EXTRACCION, nuevo_nombre)
        if not os.path.exists(nuevo_path):
            os.rename(path, nuevo_path)

    return [os.path.join(CARPETA_EXTRACCION, f) for f in os.listdir(CARPETA_EXTRACCION)
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.bmp'))]

def insertar_fotos_personas():
    print("🖼️ Insertando fotos en Personas y Empleados...")
    conn = conexion_sql('ClinicaSanna')
    cur = conn.cursor()
    archivos = extraer_fotos_renombradas()

    for ruta in archivos:
        archivo = os.path.basename(ruta)
        persona_id = os.path.splitext(archivo)[0]
        try:
            with open(ruta, 'rb') as img_file:
                binario = img_file.read()
            cur.execute("UPDATE Personas SET Fotos = ? WHERE PersonaID = ?", (binario, persona_id))
            cur.execute("UPDATE Empleados SET Fotos = ? WHERE EmpleadoID = ?", (binario, persona_id))
            print(f"✅ Foto insertada para ID: {persona_id}")
        except Exception as e:
            print(f"❌ Error insertando foto para {persona_id}: {e}")
    conn.commit()
    conn.close()

def importar_personas():
    print("🔄 Importando Personas...")
    xl = pd.ExcelFile(EXCEL_FILE, engine='openpyxl')
    df = xl.parse('TemPersonas', dtype=str)
    df.columns = df.columns.str.strip()

    conn = conexion_sql('ClinicaSanna')
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute("SELECT COUNT(*) FROM Personas WHERE PersonaID = ?", row["PersonaID"])
        if cur.fetchone()[0] == 0:
            raw_fecha = row["FechaNacimiento"].strip() if pd.notnull(row["FechaNacimiento"]) else None
            fecha_nac = pd.to_datetime(raw_fecha, errors='coerce', dayfirst=True)
            fecha_nac_sql = fecha_nac.date() if pd.notnull(fecha_nac) else None

            try:
                cur.execute("""
                    INSERT INTO Personas (
                        PersonaID, Nombre, Apellido, FechaNacimiento,
                        GeneroID, TipoPersona, TipoSangreID, DiagnosticoID, UbigeoID, FotoID
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    row["PersonaID"], row["Nombre"], row["Apellido"], fecha_nac_sql,
                    row["GeneroID"], row["TipoPersona"], row["TipoSangreID"],
                    row["DiagnosticoID"], row["UbigeoID"], row["FotoID"]
                ])
                print(f"✅ Persona insertada: {row['PersonaID']}")
            except Exception as e:
                print(f"❌ Error insertando {row['PersonaID']} | Error: {e}")
        else:
            print(f"ℹ️ Persona ya existe: {row['PersonaID']}")

    conn.commit()
    conn.close()

def importar_empleados():
    print("🔄 Importando Empleados...")
    xl = pd.ExcelFile(EXCEL_FILE, engine='openpyxl')
    df = xl.parse('Empleados', dtype=str)
    df.columns = df.columns.str.strip()

    conn = conexion_sql('ClinicaSanna')
    cur = conn.cursor()

    for _, row in df.iterrows():
        cur.execute("SELECT COUNT(*) FROM Empleados WHERE EmpleadoID = ?", row["EmpleadoID"])
        if cur.fetchone()[0] == 0:
            raw_fecha = row["FechaIngreso"].strip() if pd.notnull(row["FechaIngreso"]) else None
            fecha_ingreso = pd.to_datetime(raw_fecha, errors='coerce', dayfirst=True)
            fecha_ingreso_sql = fecha_ingreso.date() if pd.notnull(fecha_ingreso) else None

            try:
                cur.execute("""
                    INSERT INTO Empleados (
                        EmpleadoID, NombreEmpleado, Cargo, FechaIngreso,
                        SucursalID, UbigeoID, Diagnostico, FotoID
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    row["EmpleadoID"], row["NombreEmpleado"], row["Cargo"], fecha_ingreso_sql,
                    row["SucursalID"], row["UbigeoID"], row["Diagnostico"], row["FotoID"]
                ])
                print(f"✅ Empleado insertado: {row['EmpleadoID']}")
            except Exception as e:
                print(f"❌ Error insertando empleado {row['EmpleadoID']} | Error: {e}")
        else:
            print(f"ℹ️ Empleado ya existe: {row['EmpleadoID']}")

    conn.commit()
    conn.close()

def migrar_empleados():
    print("🔄 Migrando empleados a INDICE_DE_EFICIENCIA_FINANCIERA...")
    conn = conexion_sql('ClinicaSanna')
    cur = conn.cursor()

    cur.execute("""
        SELECT E.EmpleadoID, E.NombreEmpleado, E.Cargo, E.Diagnostico, E.FechaIngreso, E.Fotos
        FROM Empleados E
    """)
    empleados = cur.fetchall()

    conn_dest = conexion_sql('INDICE_DE_EFICIENCIA_FINANCIERA')
    cur_dest = conn_dest.cursor()

    for emp in empleados:
        try:
            cur_dest.execute("SELECT COUNT(*) FROM Empleado_Dim WHERE id_empleado = ?", emp[0])
            existe = cur_dest.fetchone()[0]

            if existe == 0:
                cur_dest.execute("""
                    INSERT INTO Empleado_Dim (
                        id_empleado, nombre_empleado, cargo_empleado,
                        diagnostico_empleado, fecha_ingreso_empleado, foto_empleado
                    ) VALUES (?, ?, ?, ?, ?, ?)
                """, emp)
                print(f"✅ Empleado migrado: {emp[0]}")
            else:
                cur_dest.execute("""
                    UPDATE Empleado_Dim
                    SET nombre_empleado = ?, cargo_empleado = ?, diagnostico_empleado = ?,
                        fecha_ingreso_empleado = ?, foto_empleado = ?
                    WHERE id_empleado = ?
                """, (emp[1], emp[2], emp[3], emp[4], emp[5], emp[0]))
                print(f"🔄 Empleado actualizado: {emp[0]}")
        except Exception as e:
            print(f"❌ Error con empleado {emp[0]} | Error: {e}")

    conn_dest.commit()
    conn_dest.close()
    conn.close()

if __name__ == "__main__":
    importar_personas()
    insertar_fotos_personas()
    importar_empleados()
    migrar_empleados()
