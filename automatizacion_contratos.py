import pandas as pd
import pyodbc
import os

server = 'DESKTOP-DHTBPN6\\SQLSERVER2022'
user = 'Eficiencia'
password = '1234'
database = 'ClinicaSanna'
driver = '{ODBC Driver 17 for SQL Server}'

def simular_descarga():
    print("Descarga de contratos desde la web...")

    contratos_simulados = []
    for i in range(1, 136): 
        contratos_simulados.append({
            'ContratoID': f'CON{i:03}',
            'Fecha_Inicio': '2024-01-01',
            'Fecha_Fin': '2024-12-31',
            'Tipo': 'Servicio',
            'Estado': 'Vigente',
            'ProveedorID': f'P{(i % 10 + 1):03}',       
            'CapacitacionID': f'C{(i % 10 + 1):03}'    
        })

    df = pd.DataFrame(contratos_simulados)
    archivo = 'Contrato.xlsx'
    with pd.ExcelWriter(archivo, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='TeamContrato', index=False)

    print(f"Archivo generado: {archivo} (hoja: TeamContrato) con {len(df)} contratos")

def leer_excel():
    print("Leyendo datos desde Contrato.xlsx (hoja: TeamContrato)...")
    archivo = 'Contrato.xlsx'
    if not os.path.exists(archivo):
        print("Archivo Excel no encontrado.")
        return pd.DataFrame()

    try:
        df = pd.read_excel(archivo, sheet_name='TeamContrato', dtype=str)
        df.fillna('', inplace=True)
        return df
    except Exception as e:
        print(f"Error leyendo el archivo Excel: {e}")
        return pd.DataFrame()

def insertar_actualizar_contratos(df):
    print("Insertando/actualizando contratos en ClinicaSanna...")
    conn = pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password}'
    )
    cursor = conn.cursor()
    total = 0

    for idx, row in df.iterrows():
        try:
            cursor.execute("""
                IF EXISTS (SELECT 1 FROM Legal.Contratos WHERE ContratoID = ?)
                BEGIN
                    UPDATE Legal.Contratos SET
                        FechaInicio = ?, FechaFin = ?, Tipo = ?, Estado = ?, 
                        ProveedorID = ?, CapacitacionID = ?
                    WHERE ContratoID = ?
                END
                ELSE
                BEGIN
                    INSERT INTO Legal.Contratos
                    (ContratoID, FechaInicio, FechaFin, Tipo, Estado, ProveedorID, CapacitacionID)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                END
            """, (
                row.ContratoID,
                row.Fecha_Inicio, row.Fecha_Fin, row.Tipo, row.Estado, row.ProveedorID, row.CapacitacionID, row.ContratoID,  # UPDATE
                row.ContratoID, row.Fecha_Inicio, row.Fecha_Fin, row.Tipo, row.Estado, row.ProveedorID, row.CapacitacionID   # INSERT
            ))
            total += 1
        except Exception as e:
            print(f"Error con {row.ContratoID}: {e}")

    conn.commit()
    cursor.close()
    conn.close()
    print(f"Contratos insertados o actualizados: {total}")

# Migrar a dimensión Contrato_Dim
def migrar_a_dim():
    print("Migrando contratos a la dimensión Contrato_Dim...")
    try:
        conn = pyodbc.connect(
            f'DRIVER={driver};SERVER={server};DATABASE={database};UID={user};PWD={password}'
        )
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Contrato_Dim
            (id_contrato, tipo_contrato, estado_contrato)
            SELECT C.ContratoID, C.Tipo, C.Estado
            FROM Legal.Contratos C
            WHERE NOT EXISTS (
                SELECT 1 FROM [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Contrato_Dim D
                WHERE D.id_contrato = C.ContratoID
            )
        """)
        rows = cursor.rowcount
        conn.commit()
        print(f"Contratos migrados a dimensión: {rows}")
        cursor.close()
        conn.close()
    except Exception as e:
        print(f"Error en migración a dimensión: {e}")

# Main
def main():
    simular_descarga()
    df = leer_excel()
    if df.empty:
        print("No hay contratos para procesar.")
        return
    insertar_actualizar_contratos(df)
    migrar_a_dim()
    print("Proceso completo.")

if __name__ == "__main__":
    main()
