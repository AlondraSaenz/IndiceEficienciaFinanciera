# README - IndiceEficienciaFinanciera
Este proyecto permite medir la eficiencia en el uso de los recursos financieros en Clínica Sanna, con el fin de optimizar la gestión operativa y mejorar la atención al paciente.

# Descripción
El repositorio contiene scripts en Python que automatizan la descarga de distintos tipos de datos (contratos, fotos, pagos, transferencias, textos, entre otros) y los integran en una base de datos SQL Server para generar un índice de eficiencia financiera.

# Requisitos
- Python 3.8 o superior
- SQL Server (local o remoto)
- Visual Studio Code (VS Code)
- Conexión a Internet

# Paquetes recomendados
Este proyecto requiere algunos paquetes para funcionar correctamente. Puedes instalarlos con el siguiente comando:
 
  pip install pandas pyodbc requests openpyxl
  
# Si usas un entorno virtual (recomendado), crea uno primero con:
python -m venv venv
venv\Scripts\activate    # En Windows
source venv/bin/activate   # En Linux/Mac

# Y luego instala los paquetes como se indicó.

# Instalación
1. Clona este repositorio:
git clone https://github.com/AlondraSaenz/IndiceEficienciaFinanciera.git

2. Abre la carpeta del proyecto con Visual Studio Code.

3. Instala los paquetes necesarios (si aún no lo hiciste):

    pip install pandas pyodbc requests openpyxl

# También puedes crear un archivo requirements.txt y ejecutarlo así:

    pip install -r requirements.txt

# Ejecuta los scripts según los datos que necesites automatizar:
  python automatizacion_contratos.py
  python automatizacion_fotos.py
  python automatizacion_pagos.py
  python automatizacion_transferencias.py
  python automatizacion_redes.py
  python automatizacion_textos.py
  python automatizacion_web.py

Los datos procesados serán dirigidos automáticamente al archivo INDICE_DE_EFICIENCIA_FINANCIERA.xlsx y/o a la base de datos SQL Server configurada.

# Estudiantes de la universidad Cesar Vallejo - Trujillo Olivos

# Autores:
- Alvarez Rojales, Nilson Esmilver (0000-0001-7798-0551)
- Montoya Contreras, Jenyfer Tatiana (0000-0003-2035-3316)
- Saenz Nuñez, Alondra Leonela (0000-0003-4962-3172)
- Tesen Chavez, Kevin Jhon(/0000-0001-5132-5866)

Repositorio creado con fines educativos para aprender la implementación de procesos de automatización en la gestión financiera, utilizando datos simulados inspirados en la Clínica Sanna.
