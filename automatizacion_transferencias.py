import pandas as pd
import pyodbc
import datetime

EXCEL_FILE = r"C:\Users\USUARIO\Downloads\Transferencias.xlsx"
server = 'DESKTOP-DHTBPN6\\SQLSERVER2022'
user = 'Eficiencia'
password = '1234'
driver = '{ODBC Driver 17 for SQL Server}'

def conexion_sql(db):
    return pyodbc.connect(
        f'DRIVER={driver};SERVER={server};DATABASE={db};UID={user};PWD={password}'
    )

def importar_transacciones():
    print("Importando Transacciones desde Excel...")

    df = pd.read_excel(EXCEL_FILE, sheet_name='TemTransferencias', dtype=str).fillna('')
    df.columns = df.columns.str.strip()

    conn = conexion_sql('ClinicaSanna')
    cur = conn.cursor()

    for _, row in df.iterrows():
        transaccion_id = row["TransaccionID"]
        cita_id = row["CitaID"]

        cur.execute("SELECT COUNT(*) FROM Finanzas.Transacciones WHERE TransaccionID = ?", transaccion_id)
        existe = cur.fetchone()[0]

        # Validar FK a CitaID
        if cita_id:
            cur.execute("SELECT COUNT(*) FROM Administracion.Citas WHERE CitaID = ?", cita_id)
            if cur.fetchone()[0] == 0:
                print(f"Transacción {transaccion_id} omitida: CitaID '{cita_id}' no existe.")
                continue

        try:
            fecha_sql = pd.to_datetime(row["Fecha"], errors='coerce', dayfirst=True).date()
            # Limpieza y conversión del monto
            monto_str = str(row["Monto"]).replace(",", "").replace("S/", "").strip()
            monto_val = float(monto_str) if monto_str else 0.0

            if existe == 0:
                cur.execute("""
                    INSERT INTO Finanzas.Transacciones (
                        TransaccionID, Fecha, Monto, Tipo, Descripcion,
                        SucursalID, CitaID, PacienteID, MetodoPago, Estado
                    )
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, [
                    transaccion_id, fecha_sql, monto_val, row["Tipo"] or None,
                    row["Descripcion"] or None, row["SucursalID"] or None,
                    cita_id or None, row["PacienteID"] or None,
                    row["MetodoPago"] or None, row["Estado"] or None
                ])
                print(f"Transacción insertada: {transaccion_id}")
            else:
                cur.execute("""
                    UPDATE Finanzas.Transacciones SET
                        Fecha = ?, Monto = ?, Tipo = ?, Descripcion = ?, 
                        SucursalID = ?, CitaID = ?, PacienteID = ?, 
                        MetodoPago = ?, Estado = ?
                    WHERE TransaccionID = ?
                """, [
                    fecha_sql, monto_val, row["Tipo"] or None, row["Descripcion"] or None,
                    row["SucursalID"] or None, cita_id or None, row["PacienteID"] or None,
                    row["MetodoPago"] or None, row["Estado"] or None, transaccion_id
                ])
                print(f"Transacción actualizada: {transaccion_id}")
        except Exception as e:
            print(f"Error con transacción {transaccion_id} | Error: {e}")

    conn.commit()
    conn.close()

def migrar_transacciones():
    print("Migrando a INDICE_DE_EFICIENCIA_FINANCIERA...")

    conn = conexion_sql('ClinicaSanna')
    cur = conn.cursor()

    cur.execute("""
        SELECT TransaccionID, Tipo, Descripcion, Estado, MetodoPago, Monto
        FROM Finanzas.Transacciones
    """)
    trans = cur.fetchall()

    conn_dest = conexion_sql('INDICE_DE_EFICIENCIA_FINANCIERA')
    cur_dest = conn_dest.cursor()

    for tr in trans:
        id_transaccion = tr[0]
        tipo = str(tr[1]) if tr[1] else None
        descripcion = str(tr[2]) if tr[2] else None
        estado = str(tr[3]) if tr[3] else None
        metodo_pago = str(tr[4]) if tr[4] else None

        try:
            monto_raw = str(tr[5]).replace(",", "").replace("S/", "").strip()
            monto_val = float(monto_raw) if monto_raw else 0.0
        except:
            print(f"Error al convertir monto de {id_transaccion}. Se usará 0.0")
            monto_val = 0.0

        # Verificar si existe en la tabla destino
        cur_dest.execute("SELECT COUNT(*) FROM Transaccion_Dim WHERE id_transaccion = ?", id_transaccion)
        if cur_dest.fetchone()[0] == 0:
            cur_dest.execute("""
                INSERT INTO Transaccion_Dim (
                    id_transaccion, tipo_transaccion, descripcion_transaccion,
                    estado_transaccion, metodo_pago, monto_transaccion
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (id_transaccion, tipo, descripcion, estado, metodo_pago, monto_val))
            print(f"Migrada: {id_transaccion}")
        else:
            cur_dest.execute("""
                UPDATE Transaccion_Dim SET
                    tipo_transaccion = ?, descripcion_transaccion = ?, 
                    estado_transaccion = ?, metodo_pago = ?, monto_transaccion = ?
                WHERE id_transaccion = ?
            """, (tipo, descripcion, estado, metodo_pago, monto_val, id_transaccion))
            print(f"Actualizada: {id_transaccion}")

    conn_dest.commit()
    conn.close()
    conn_dest.close()

if __name__ == "__main__":
    importar_transacciones()
    migrar_transacciones()
