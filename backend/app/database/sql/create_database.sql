Create DATABASE MesaAyudaDB;
GO

USE MesaAyudaDB;
GO
-- Tabla Cliente
CREATE TABLE Cliente (
    id_cliente INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefono VARCHAR(20),
    direccion VARCHAR(200)
);
GO

-- Tabla UsuarioSistema
CREATE TABLE UsuarioSistema (
    id_usuario INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefono VARCHAR(20),
    rol VARCHAR(50), -- tecnico, supervisor, admin
    especialidad VARCHAR(100) -- opcional, solo para técnicos
);
GO

-- Tabla TipoServicio
CREATE TABLE TipoServicio (
    id_tipo INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);
GO

-- Tabla ServicioCliente
CREATE TABLE ServicioCliente (
    id_servicio INT IDENTITY(1,1) PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_tipo INT NOT NULL,
    fecha_inicio DATE,
    estado VARCHAR(50),
    CONSTRAINT FK_ServicioCliente_Cliente FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
    CONSTRAINT FK_ServicioCliente_TipoServicio FOREIGN KEY (id_tipo) REFERENCES TipoServicio(id_tipo)
);
GO

-- Tabla TipoProblema
CREATE TABLE TipoProblema (
    id_tipo INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT
);
GO

-- Tabla Trabajo
CREATE TABLE Trabajo (
    id_trabajo INT IDENTITY(1,1) PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_tecnico INT NOT NULL,
    id_tipo INT NOT NULL,
    fecha_creacion DATETIME,
    estado VARCHAR(50),
    tipo_problema VARCHAR(100), -- redundante para consultas rápidas
    CONSTRAINT FK_Trabajo_Cliente FOREIGN KEY (id_cliente) REFERENCES Cliente(id_cliente),
    CONSTRAINT FK_Trabajo_UsuarioSistema FOREIGN KEY (id_tecnico) REFERENCES UsuarioSistema(id_usuario),
    CONSTRAINT FK_Trabajo_TipoProblema FOREIGN KEY (id_tipo) REFERENCES TipoProblema(id_tipo)
);
GO

-- Tabla DetalleTrabajo
CREATE TABLE DetalleTrabajo (
    id_detalle INT IDENTITY(1,1) PRIMARY KEY,
    id_trabajo INT NOT NULL,
    tipo VARCHAR(50),
    descripcion TEXT,
    CONSTRAINT FK_DetalleTrabajo_Trabajo FOREIGN KEY (id_trabajo) REFERENCES Trabajo(id_trabajo)
);
GO

-- Tabla EquipoInstalado
CREATE TABLE EquipoInstalado (
    id_equipo INT IDENTITY(1,1) PRIMARY KEY,
    id_trabajo INT NOT NULL,
    modelo VARCHAR(100),
    serie VARCHAR(100),
    fecha_instalacion DATE,
    CONSTRAINT FK_EquipoInstalado_Trabajo FOREIGN KEY (id_trabajo) REFERENCES Trabajo(id_trabajo)
);
GO

-- Tabla Catalogo
CREATE TABLE Catalogo (
    id_catalogo INT IDENTITY(1,1) PRIMARY KEY,
    nombre VARCHAR(100),
    descripcion TEXT,
    tipo VARCHAR(50), -- problemas, categorías, motivos_cierre
    creado_por INT,
    CONSTRAINT FK_Catalogo_UsuarioSistema FOREIGN KEY (creado_por) REFERENCES UsuarioSistema(id_usuario)
);
GO

-- Tabla Ticket
CREATE TABLE Ticket (
    id_ticket INT IDENTITY(1,1) PRIMARY KEY,
    id_trabajo INT NOT NULL,
    creado_por INT NOT NULL,
    id_catalogo INT NOT NULL,
    fecha_creado DATETIME,
    estado VARCHAR(50),
    prioridad VARCHAR(20), -- alta, media, baja
    CONSTRAINT FK_Ticket_Trabajo FOREIGN KEY (id_trabajo) REFERENCES Trabajo(id_trabajo),
    CONSTRAINT FK_Ticket_UsuarioSistema FOREIGN KEY (creado_por) REFERENCES UsuarioSistema(id_usuario),
    CONSTRAINT FK_Ticket_Catalogo FOREIGN KEY (id_catalogo) REFERENCES Catalogo(id_catalogo)
);
GO

-- Tabla Validacion
CREATE TABLE Validacion (
    id_validacion INT IDENTITY(1,1) PRIMARY KEY,
    id_ticket INT NOT NULL,
    id_supervisor INT NOT NULL,
    fecha_validacion DATETIME,
    resultado BIT,
    observaciones TEXT,
    CONSTRAINT FK_Validacion_Ticket FOREIGN KEY (id_ticket) REFERENCES Ticket(id_ticket),
    CONSTRAINT FK_Validacion_UsuarioSistema FOREIGN KEY (id_supervisor) REFERENCES UsuarioSistema(id_usuario)
);
GO

-- Tabla HistorialTicket
CREATE TABLE HistorialTicket (
    id_historial INT IDENTITY(1,1) PRIMARY KEY,
    id_ticket INT NOT NULL,
    fecha DATETIME,
    estado_anterior VARCHAR(50),
    estado_nuevo VARCHAR(50),
    comentario TEXT,
    CONSTRAINT FK_HistorialTicket_Ticket FOREIGN KEY (id_ticket) REFERENCES Ticket(id_ticket)
);
GO