import pandas as pd
import pyodbc
import re

conn_str_origen = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-DHTBPN6\\SQLSERVER2022;'
    'DATABASE=ClinicaSanna;'
    'UID=Eficiencia;PWD=1234'
)
conn_str_destino = (
    'DRIVER={ODBC Driver 17 for SQL Server};'
    'SERVER=DESKTOP-DHTBPN6\\SQLSERVER2022;'
    'DATABASE=INDICE_DE_EFICIENCIA_FINANCIERA;'
    'UID=Eficiencia;PWD=1234'
)

excel_path = r'C:\Users\USUARIO\Downloads\pago.xlsx'
df_pago = pd.read_excel(excel_path, sheet_name='TemPago')

def limpiar_monto(monto_str):
    if isinstance(monto_str, (int, float)):
        return float(monto_str)
    # Eliminar "S/" y espacios, cambiar "," a vacío y "." a punto decimal si es necesario
    monto_str = str(monto_str).replace('S/', '').replace(' ', '').replace(',', '')
    try:
        return float(monto_str)
    except:
        return 0.0

conn_origen = pyodbc.connect(conn_str_origen)
cursor_origen = conn_origen.cursor()

conn_destino = pyodbc.connect(conn_str_destino)
cursor_destino = conn_destino.cursor()

print("Verificando e insertando pagos en Finanzas.Pagos...")

for index, row in df_pago.iterrows():
    pago_id = row['PagoID']
    cita_id = row['CitaID']
    fecha_pago = row['FechaPago']
    monto = limpiar_monto(row['MontoTotal'])
    estado = row['Estado']

    # Verificar si existe PagoID en Finanzas.Pagos
    cursor_origen.execute("SELECT 1 FROM Finanzas.Pagos WHERE PagoID = ?", (pago_id,))
    existe_pago = cursor_origen.fetchone()

    if not existe_pago:
        # Insertar nuevo pago
        try:
            cursor_origen.execute("""
                INSERT INTO Finanzas.Pagos (PagoID, CitaID, FechaPago, MontoTotal, Estado)
                VALUES (?, ?, ?, ?, ?)
            """, (pago_id, cita_id, fecha_pago, monto, estado))
            print(f"Pago insertado: {pago_id}")
        except Exception as e:
            print(f"Error insertando pago {pago_id}: {e}")
    else:
        # Actualizar pago existente
        try:
            cursor_origen.execute("""
                UPDATE Finanzas.Pagos
                SET CitaID = ?, FechaPago = ?, MontoTotal = ?, Estado = ?
                WHERE PagoID = ?
            """, (cita_id, fecha_pago, monto, estado, pago_id))
            print(f"Pago actualizado: {pago_id}")
        except Exception as e:
            print(f"Error actualizando pago {pago_id}: {e}")

conn_origen.commit()

# Migración de fechas a la base destino con INSERT INTO ... SELECT DISTINCT ...
migracion_fechas_sql = """
INSERT INTO [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Fecha_Dim (
    año_mes,
    dia_semana,
    trimestre,
    dia_año,
    semana_año,
    mes,
    año,
    fecha
)
SELECT DISTINCT
    DATENAME(MONTH, P.FechaPago) + '_' + CAST(YEAR(P.FechaPago) AS VARCHAR) AS año_mes,
    DATENAME(WEEKDAY, P.FechaPago) AS dia_semana,
    DATEPART(QUARTER, P.FechaPago) AS trimestre,
    DATEPART(DAYOFYEAR, P.FechaPago) AS dia_año,
    DATEPART(WEEK, P.FechaPago) AS semana_año,
    DATEPART(MONTH, P.FechaPago) AS mes,
    YEAR(P.FechaPago) AS año,
    CAST(P.FechaPago AS DATE) AS fecha
FROM [ClinicaSanna].Finanzas.Pagos P
WHERE NOT EXISTS (
    SELECT 1 FROM [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Fecha_Dim FD WHERE FD.fecha = CAST(P.FechaPago AS DATE)
)
"""

cursor_destino.execute(migracion_fechas_sql)
conn_destino.commit()
print("Migración de fechas completada.")

# Cerrar conexiones
cursor_origen.close()
conn_origen.close()
cursor_destino.close()
conn_destino.close()

print("Proceso finalizado con éxito.")
