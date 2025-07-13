import os
import tarfile
from PIL import Image, UnidentifiedImageError
import gdown
import pyodbc

server = 'DESKTOP-DHTBPN6\\SQLSERVER2022'  # Ajusta a tu servidor
user = 'Eficiencia'
password = '1234'
driver = '{ODBC Driver 17 for SQL Server}'

def conexion_sql(db):
    return pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={db};UID={user};PWD={password}'
    )

def descargar_tar_gz_drive(drive_id, output_path):
    if os.path.exists(output_path):
        print("🔁 Archivo ya descargado.")
        return
    url = f"https://drive.google.com/uc?id={drive_id}"
    gdown.download(url, output_path, quiet=False, fuzzy=True)

def verificar_tar_gz(file_path):
    if not tarfile.is_tarfile(file_path):
        raise tarfile.ReadError("Archivo .tar.gz no válido.")

def descomprimir_tar_gz(file_path, extract_to):
    with tarfile.open(file_path, "r:gz") as tar:
        tar.extractall(path=extract_to)

def insertar_imagen_sql(nombre, binario, conn):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO dbo.Fotos (Nombre, Imagen) OUTPUT INSERTED.Id VALUES (?, ?)",
        nombre, binario
    )
    foto_id = cur.fetchone()[0]
    conn.commit()
    return foto_id

def convertir_y_insertar_fotos(ruta_fotos, limite=100):
    extensiones = ['.jpg', '.jpeg', '.png']
    count = 0
    conn = conexion_sql('ClinicaSanna')
    for root, _, files in os.walk(ruta_fotos):
        for file in files:
            if count >= limite:
                conn.close()
                return
            ext = os.path.splitext(file)[1].lower()
            if ext in extensiones:
                path = os.path.join(root, file)
                try:
                    with Image.open(path) as img:
                        img = img.convert("RGB")
                        img.thumbnail((100, 100))
                        tmp = os.path.join("C:\\Windows\\Temp", file + ".png")
                        img.save(tmp, format='PNG')
                        with open(tmp, 'rb') as f:
                            data = f.read()
                            foto_id = insertar_imagen_sql(file, data, conn)
                            print(f"Insertado imagen: {file} -> FotoID {foto_id}")
                            count += 1
                except (UnidentifiedImageError, OSError):
                    print(f"Error procesando {path}")
    conn.close()

# === 2. MIGRACIÓN DE EMPLEADOS A DIMENSIÓN ===
def migrar_empleados_a_dim():
    origen = conexion_sql('ClinicaSanna')
    destino = conexion_sql('INDICE_DE_EFICIENCIA_FINANCIERA')

    # Selecciona datos de Empleados según tu tabla
    select_query = (
        "SELECT EmpleadoID, NombreEmpleado, Cargo, Diagnostico, FechaIngreso "
        "FROM dbo.Empleados"
    )
    insert_query = (
        "INSERT INTO dbo.Empleado_Dim "
        "(id_empleado, nombre_empleado, cargo_empleado, diagnostico_empleado, fecha_ingreso_empleado) "
        "VALUES (?, ?, ?, ?, ?)"
    )

    cur_o = origen.cursor()
    cur_d = destino.cursor()
    for row in cur_o.execute(select_query):
        # Verifica no duplicar
        cur_d.execute("SELECT COUNT(*) FROM dbo.Empleado_Dim WHERE id_empleado = ?", row.EmpleadoID)
        if cur_d.fetchone()[0] == 0:
            cur_d.execute(insert_query,
                          row.EmpleadoID,
                          row.NombreEmpleado,
                          row.Cargo,
                          row.Diagnostico,
                          row.FechaIngreso)
            print(f"Migrado Empleado: {row.EmpleadoID}")
    destino.commit()
    origen.close()
    destino.close()
    print("Migración de empleados completada.")

if __name__ == '__main__':
    # Procesar imágenes y subir a Fotos
    drive_id = '1mb5Z24TsnKI3ygNIlX6ZFiwUj0_PmpAW'
    archivo = 'rostros.tar.gz'
    carpeta = 'rostros_extraidos'

    os.makedirs(carpeta, exist_ok=True)
    print("Descargando archivo...")
    descargar_tar_gz_drive(drive_id, archivo)
    print("Verificando...")
    verificar_tar_gz(archivo)
    print("Descomprimiendo...")
    descomprimir_tar_gz(archivo, carpeta)
    print("Insertando imágenes a la tabla Fotos...")
    convertir_y_insertar_fotos(carpeta)

    # Migrar empleados a la dimensión
    print("Iniciando migración de empleados...")
    migrar_empleados_a_dim()
