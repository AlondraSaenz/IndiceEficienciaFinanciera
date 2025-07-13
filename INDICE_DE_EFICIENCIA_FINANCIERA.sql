
use INDICE_DE_EFICIENCIA_FINANCIERA
go

--Object:  Table [dbo].[Sucursal_Dim]    
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Sucursal_Dim](
        [id_sucursal] [nvarchar](8) NOT NULL,
        [nombre_sucursal] [nvarchar](100) NOT NULL,
        [ciudad_sucursal] [nvarchar](50) NOT NULL,
        [telefono_sucursal] [nchar](9) NOT NULL,
        [direccion_sucursal] [nvarchar](150) NOT NULL,
 CONSTRAINT [PK_Sucursal_Dim] PRIMARY KEY CLUSTERED 
(
        [id_sucursal] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
SELECT * FROM Empleado_Dim
GO
--Object:  Table [dbo].[Empleado_Dim]    
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Empleado_Dim](
        [id_empleado] [nvarchar](8) NOT NULL,
		[nombre_empleado][nvarchar](50) ,
        [cargo_empleado] [nvarchar](50) NOT NULL,
        [diagnostico_empleado] [nvarchar](200) NOT NULL,
        [fecha_ingreso_empleado] [date] NULL,

 CONSTRAINT [PK_Empleado_Dim] PRIMARY KEY CLUSTERED 
(
        [id_empleado] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE Empleado_Dim
ADD foto_empleado varbinary(max);


--Object:  Table [dbo].[Contrato_Dim]    
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Contrato_Dim](
        [id_contrato] [nvarchar](8) NOT NULL,
        [tipo_contrato] [nvarchar](100) NOT NULL,
        [estado_contrato] [nvarchar](50) NOT NULL,
		 ContratoID nvarchar(8),
 CONSTRAINT [PK_Contrato_Dim] PRIMARY KEY CLUSTERED 
(
        [id_contrato] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

--Table [dbo].[Transaccion_Dim]    
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Transaccion_Dim](
        [id_transaccion] [nvarchar](8) NOT NULL,
        [tipo_transaccion] [nvarchar](50) NOT NULL,
        [descripcion_transaccion] [nvarchar](200) NOT NULL,
        [estado_transaccion] [nvarchar](50) NOT NULL, 
        [metodo_pago] [nvarchar](50) NOT NULL,  
 CONSTRAINT [PK_Transaccion_Dim] PRIMARY KEY CLUSTERED 
(
        [id_transaccion] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Transaccion_Dim]
ADD [monto_transaccion] [decimal](10,2) NOT NULL;
GO

--Table [dbo].[Pago_Dim]   
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Pago_Dim](
        [id_pago] [nvarchar](8) NOT NULL,
        [estado_pago] [nvarchar](50) NOT NULL,
 CONSTRAINT [PK_Pago_Dim] PRIMARY KEY CLUSTERED 
(
        [id_pago] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO
ALTER TABLE [dbo].[Pago_Dim]
ADD [monto_pago] [decimal](10,2) NOT NULL;
GO
--Object:  Table [dbo].[Fecha_Dim]    
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
-- Fecha_Dim
CREATE TABLE [dbo].[Fecha_Dim](
        [id_fecha] [int] IDENTITY(1,1) NOT NULL,
        [año_mes] [nchar](61) NOT NULL,
        [dia_semana] [nchar](30) NOT NULL,
        [trimestre] [int] NOT NULL,
        [dia_año] [int] NOT NULL,
        [semana_año] [int] NOT NULL,
        [mes] [int] NOT NULL,
        [año] [int] NOT NULL,
        [fecha] [date] NOT NULL,
 CONSTRAINT [PK_Fecha_Dim] PRIMARY KEY CLUSTERED 
(
        [id_fecha] ASC
)
	WITH (PAD_INDEX  = OFF, 
	STATISTICS_NORECOMPUTE  = OFF, 
	IGNORE_DUP_KEY = OFF, 
	ALLOW_ROW_LOCKS  = ON, 
	ALLOW_PAGE_LOCKS  = ON) 
		ON [PRIMARY]
) ON [PRIMARY]
GO

--Table [dbo].[Hechos_Eficiencia_Financiera]    
SET ANSI_NULLS ON
GO
SET QUOTED_IDENTIFIER ON
GO
CREATE TABLE [dbo].[Hechos_Eficiencia_Financiera](
        [id_sucursal] [nvarchar](8) NOT NULL,
        [id_empleado] [nvarchar](8) NOT NULL,
        [id_contrato] [nvarchar](8) NOT NULL,
        [id_transaccion] [nvarchar](8) NOT NULL,
        [id_pago] [nvarchar](8) NOT NULL,
        [id_fecha] [int] NOT NULL,
        [Monto_pago] [money] NOT NULL,
        [Monto_transaccion] [money] NOT NULL,
 CONSTRAINT [PK_Hechos_Eficiencia_Financiera] PRIMARY KEY CLUSTERED 
(
        [id_sucursal] ASC,
        [id_empleado] ASC,
        [id_contrato] ASC,
        [id_transaccion] ASC,
        [id_pago] ASC,
        [id_fecha] ASC
)WITH (PAD_INDEX  = OFF, STATISTICS_NORECOMPUTE  = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS  = ON, ALLOW_PAGE_LOCKS  = ON) ON [PRIMARY]
) ON [PRIMARY]
GO

--Object:  ForeignKey [FK_Hechos_Eficiencia_Financiera_Sucursal_Dim]
ALTER TABLE [dbo].[Hechos_Eficiencia_Financiera]  WITH CHECK ADD  CONSTRAINT [FK_Hechos_Eficiencia_Financiera_Sucursal_Dim] FOREIGN KEY([id_sucursal])
REFERENCES [dbo].[Sucursal_Dim] ([id_sucursal])
GO
ALTER TABLE [dbo].[Hechos_Eficiencia_Financiera] CHECK CONSTRAINT [FK_Hechos_Eficiencia_Financiera_Sucursal_Dim]
GO
/* Object:  ForeignKey [FK_Hechos_Eficiencia_Financiera_Empleado_Dim]    */
ALTER TABLE [dbo].[Hechos_Eficiencia_Financiera]  WITH CHECK ADD  CONSTRAINT [FK_Hechos_Eficiencia_Financiera_Empleado_Dim] FOREIGN KEY([id_empleado])
REFERENCES [dbo].[Empleado_Dim] ([id_empleado])
GO
ALTER TABLE [dbo].[Hechos_Eficiencia_Financiera] CHECK CONSTRAINT [FK_Hechos_Eficiencia_Financiera_Empleado_Dim]
GO
/* Object:  ForeignKey [FK_Hechos_Eficiencia_Financiera_Contrato_Dim]    */
ALTER TABLE [dbo].[Hechos_Eficiencia_Financiera]  WITH CHECK ADD  CONSTRAINT [FK_Hechos_Eficiencia_Financiera_Contrato_Dim] FOREIGN KEY([id_contrato])
REFERENCES [dbo].[Contrato_Dim] ([id_contrato])
GO
ALTER TABLE [dbo].[Hechos_Eficiencia_Financiera] CHECK CONSTRAINT [FK_Hechos_Eficiencia_Financiera_Contrato_Dim]
GO
/* Object:  ForeignKey [FK_Hechos_Ef|iciencia_Financiera_Transaccion_Dim]    */
ALTER TABLE [dbo].[Hechos_Eficiencia_Financiera]  WITH CHECK ADD  CONSTRAINT [FK_Hechos_Eficiencia_Financiera_Transaccion_Dim] FOREIGN KEY([id_transaccion])
REFERENCES [dbo].[Transaccion_Dim] ([id_transaccion])
GO
ALTER TABLE [dbo].[Hechos_Eficiencia_Financiera] CHECK CONSTRAINT [FK_Hechos_Eficiencia_Financiera_Transaccion_Dim]
GO

ALTER TABLE [dbo].[Hechos_Eficiencia_Financiera]  WITH CHECK ADD  CONSTRAINT [FK_Hechos_Eficiencia_Financiera_Fecha_Dim] 
FOREIGN KEY([id_fecha])
REFERENCES [dbo].[Fecha_Dim] ([id_fecha])
GO

ALTER TABLE [dbo].[Hechos_Eficiencia_Financiera] CHECK CONSTRAINT [FK_Hechos_Eficiencia_Financiera_Fecha_Dim]
GO

/* Object:  ForeignKey [FK_Hechos_Eficiencia_Financiera_Pago_Dim]    */
ALTER TABLE [dbo].[Hechos_Eficiencia_Financiera]  WITH CHECK ADD  CONSTRAINT [FK_Hechos_Eficiencia_Financiera_Pago_Dim] FOREIGN KEY([id_pago])
REFERENCES [dbo].[Pago_Dim] ([id_pago])
GO
ALTER TABLE [dbo].[Hechos_Eficiencia_Financiera] CHECK CONSTRAINT [FK_Hechos_Eficiencia_Financiera_Pago_Dim]
GO

--Dimensión Sucursal ------------------------------------------------------------------------------------------
-- origen
select 
S.SucursalID, S.Nombre, S.Ciudad, S.Telefono, S.Direccion
from [ClinicaSanna].Administracion.Sucursal S 
go
-- destino
select 
MS.id_sucursal, MS.nombre_sucursal, MS.ciudad_sucursal, MS.telefono_sucursal, MS.direccion_sucursal
from [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Sucursal_Dim MS 
go

--MIGRACIÓN DE SUCURSAL
--Tabla destino 
insert into [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Sucursal_Dim
(id_sucursal, nombre_sucursal, ciudad_sucursal, telefono_sucursal, direccion_sucursal)
--Tabla origen 
select 
S.SucursalID, S.Nombre, S.Ciudad, S.Telefono, S.Direccion
from [ClinicaSanna].Administracion.Sucursal S 
go

--Dimensión Empleado ------------------------------------------------------------------------------------------
-- origen
select 
E.EmpleadoID,E.NombreEmpleado, E.Cargo, E.Diagnostico, E.FechaIngreso
from [ClinicaSanna].dbo.Empleados E
go
-- destino
select 
ME.id_empleado,ME.nombre_empleado, ME.cargo_empleado, ME.diagnostico_empleado, ME.fecha_ingreso_empleado
from [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Empleado_Dim ME
go

INSERT INTO [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Empleado_Dim (
    id_empleado, nombre_empleado, cargo_empleado,
    diagnostico_empleado, fecha_ingreso_empleado, foto_empleado
)
SELECT 
    E.EmpleadoID,
    E.NombreEmpleado,
    E.Cargo,
    E.Diagnostico,
    E.FechaIngreso,
    E.Fotos
FROM [ClinicaSanna].dbo.Empleados E
go

--Dimensión Contrato ------------------------------------------------------------------------------------------
-- origen
select 
C.ContratoID, C.Tipo, C.Estado
from [ClinicaSanna].Legal.Contratos C
go
-- destino
select 
MC.id_contrato, MC.tipo_contrato, MC.estado_contrato
from [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Contrato_Dim MC
go

--MIGRACIÓN 
--Tabla destino 
insert into [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Contrato_Dim
(id_contrato, tipo_contrato, estado_contrato)
--Tabla origen 
select 
C.ContratoID, C.Tipo, C.Estado
from [ClinicaSanna].Legal.Contratos C
go

--Dimensión Transacción ------------------------------------------------------------------------------------------
-- origen
select 
T.TransaccionID, T.Tipo, T.Descripcion, T.Estado, T.MetodoPago, T.Monto
from [ClinicaSanna].Finanzas.Transacciones T
go
-- destino
select 
MT.id_transaccion, MT.tipo_transaccion, MT.descripcion_transaccion, MT.estado_transaccion, MT.metodo_pago, MT.monto_transaccion
from [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Transaccion_Dim MT
go

--MIGRACIÓN 
--Tabla destino 
insert into [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Transaccion_Dim
(id_transaccion, tipo_transaccion, descripcion_transaccion, estado_transaccion, metodo_pago, monto_transaccion)
--Tabla origen 
select 
T.TransaccionID, T.Tipo, T.Descripcion, T.Estado, T.MetodoPago, T.Monto
from [ClinicaSanna].Finanzas.Transacciones T
go

--Dimensión Pago ------------------------------------------------------------------------------------------
--origen
select 
P.PagoID, P.Estado, P.MontoTotal
from [ClinicaSanna].Finanzas.Pagos P
go
-- destino
select 
MP.id_pago, MP.estado_pago, MP.monto_pago
from [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Pago_Dim MP
go

--MIGRACIÓN 
--Tabla destino 
insert into [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Pago_Dim
(id_pago, estado_pago, monto_pago)
--Tabla origen 
select 
P.PagoID, P.Estado, P.MontoTotal
from [ClinicaSanna].Finanzas.Pagos P
go

-- Dimension Fecha ------------------------------------------------------------------------------------------
-- origen
select 
P.PagoID, P.FechaPago
from [ClinicaSanna].Finanzas.Pagos P
go

-- destino
select 
FD.id_fecha, FD.fecha
from [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Fecha_Dim FD
go

-- MIGRACIÓN 
-- Tabla destino 
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
-- Tabla origen 
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
GO

-- HECHOS_EFICIENCIA_FINANCIERA ----------------------------------------------------------
INSERT INTO [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Hechos_Eficiencia_Financiera (
    id_sucursal, 
    id_empleado, 
    id_contrato, 
    id_transaccion, 
    id_pago, 
    id_fecha, 
    monto_pago, 
    monto_transaccion
)
SELECT DISTINCT
    S.SucursalID AS id_sucursal,
    E.EmpleadoID AS id_empleado,
    ISNULL(C.ContratoID, 0) AS id_contrato, 
    T.TransaccionID AS id_transaccion,
    P.PagoID AS id_pago,
    FD.id_fecha AS id_fecha,
    CAST(P.MontoTotal AS DECIMAL(18,2)) AS monto_pago,
    CAST(T.Monto AS DECIMAL(18,2)) AS monto_transaccion
FROM [ClinicaSanna].Finanzas.Pagos P
INNER JOIN [ClinicaSanna].Administracion.Citas CI ON P.CitaID = CI.CitaID
INNER JOIN [ClinicaSanna].Finanzas.Transacciones T ON CI.CitaID = T.CitaID
INNER JOIN [ClinicaSanna].Administracion.Sucursal S ON T.SucursalID = S.SucursalID
INNER JOIN [ClinicaSanna].dbo.Empleados E ON E.SucursalID = S.SucursalID
LEFT JOIN [ClinicaSanna].Legal.Contratos C ON E.EmpleadoID = E.EmpleadoID  
INNER JOIN [INDICE_DE_EFICIENCIA_FINANCIERA].dbo.Fecha_Dim FD ON FD.fecha = CAST(P.FechaPago AS DATE)
WHERE 
    P.FechaPago IS NOT NULL 
    AND P.MontoTotal IS NOT NULL 
    AND T.Monto IS NOT NULL
    AND ISNUMERIC(CAST(P.MontoTotal AS VARCHAR)) = 1
    AND ISNUMERIC(CAST(T.Monto AS VARCHAR)) = 1;
GO

USE INDICE_DE_EFICIENCIA_FINANCIERA;
GO

SELECT *
FROM ComentarioInstagram_Dim
USE INDICE_DE_EFICIENCIA_FINANCIERA;
GO


SELECT id_palabra, palabra, frecuencia, fecha_registro
FROM ResumenPalabras_Dim;

SELECT id_conclusion, texto, fecha_registro
FROM AnalisisTextoConclusion_Dim;



SELECT id_palabra, palabra, frecuencia, fecha_registro
FROM ResumenPalabrasWeb_Dim;
SELECT id_conclusion, texto, fecha_registro
FROM AnalisisWebConclusion_Dim;