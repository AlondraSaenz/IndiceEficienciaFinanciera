import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker

# Configuración
fake = Faker('es_ES')
Faker.seed(0)
random.seed(0)

# ==========================
# Generar 500 Proveedores
# ==========================
proveedores = []
for i in range(1, 501):
    proveedores.append({
        "ProveedorID": f"P{i:03}",
        "Nombre": fake.company(),
        "RUC": f"{random.randint(20000000000, 20999999999)}",
        "Telefono": f"{random.randint(900000000, 999999999)}",
        "Direccion": fake.address(),
        "UbigeoID": f"{random.randint(1, 24):02}0101000001"
    })

# ==========================
# Generar 500 Capacitaciones
# ==========================
capacitaciones = []
nombres_cap = [
    "Manejo de Equipos Pesados", "Primeros Auxilios", "Bioseguridad en Clínicas",
    "Seguridad Industrial", "Gestión de Riesgos", "Electricidad Básica",
    "Soldadura Industrial", "Operación de Grúa Torre", "Logística y Almacenes", "Mantenimiento Preventivo"
]
start_date = datetime(2024, 1, 1)
end_date = datetime(2025, 12, 31)

for i in range(1, 501):
    capacitaciones.append({
        "CapacitacionID": f"C{i:03}",
        "Nombre": random.choice(nombres_cap),
        "Fecha": fake.date_between(start_date=start_date, end_date=end_date),
        "Instructor": fake.name(),
        "Descripcion": fake.sentence(nb_words=10)
    })

# ==========================
# Generar 500 Contratos
# ==========================
contratos = []
tipos = [
    "Capacitación en Seguridad", "Servicio de Consultoría", "Mantenimiento",
    "Compra de Equipos", "Servicio Técnico", "Capacitación Avanzada",
    "Consultoría Estratégica", "Mantenimiento Preventivo", "Compra de Software"
]
estados = ["Activo", "Finalizado", "Cancelado", "Renovado"]

for i in range(1, 501):
    fecha_inicio = fake.date_between(start_date=start_date, end_date=datetime(2025, 6, 30))
    fecha_fin = fecha_inicio + timedelta(days=random.randint(180, 365))
    contratos.append({
        "ContratoID": f"CON{i:03}",
        "FechaInicio": fecha_inicio,
        "FechaFin": fecha_fin,
        "Tipo": random.choice(tipos),
        "Estado": random.choice(estados),
        "ProveedorID": random.choice(proveedores)["ProveedorID"],
        "CapacitacionID": random.choice(capacitaciones)["CapacitacionID"]
    })

# ==========================
# Crear DataFrames
# ==========================
df_proveedores = pd.DataFrame(proveedores)
df_capacitaciones = pd.DataFrame(capacitaciones)
df_contratos = pd.DataFrame(contratos)

# ==========================
# Exportar a Excel
# ==========================
with pd.ExcelWriter("Base_Contratos_500.xlsx", engine='xlsxwriter') as writer:
    df_contratos.to_excel(writer, sheet_name="Contratos", index=False)
    df_proveedores.to_excel(writer, sheet_name="Proveedores", index=False)
    df_capacitaciones.to_excel(writer, sheet_name="Capacitaciones", index=False)

print("✅ Excel generado correctamente con 500 registros en cada hoja como Base_Contratos_500.xlsx")
