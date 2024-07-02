
-- Crear tabla de Roles
CREATE TABLE Roles (
    role_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    role_name VARCHAR2(50) NOT NULL
);

-- Crear tabla de Usuarios
CREATE TABLE Usuarios (
    user_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    username VARCHAR2(50) NOT NULL UNIQUE,
    password VARCHAR2(100) NOT NULL,
    role_id NUMBER,
    FOREIGN KEY (role_id) REFERENCES Roles(role_id)
);

-- Crear tabla de Residentes
CREATE TABLE Residentes (
    residente_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    nombre VARCHAR2(100) NOT NULL,
    fecha_nacimiento DATE NOT NULL,
    direccion VARCHAR2(200),
    telefono VARCHAR2(20)
);

-- Crear tabla de Farmacia
CREATE TABLE Farmacia (
    insumo_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    nombre_insumo VARCHAR2(100) NOT NULL,
    descripcion VARCHAR2(200),
    cantidad NUMBER NOT NULL
);

-- Crear tabla de Registro de Recepcion
CREATE TABLE Registro_Recepcion (
    recepcion_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    insumo_id NUMBER NOT NULL,
    cantidad_recibida NUMBER NOT NULL,
    fecha_recepcion DATE NOT NULL,
    usuario_id NUMBER NOT NULL,
    FOREIGN KEY (insumo_id) REFERENCES Farmacia(insumo_id),
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(user_id)
);

-- Crear tabla de Acceso
CREATE TABLE Acceso (
    acceso_id NUMBER GENERATED BY DEFAULT AS IDENTITY PRIMARY KEY,
    usuario_id NUMBER NOT NULL,
    entidad VARCHAR2(50) NOT NULL,
    entidad_id NUMBER NOT NULL,
    fecha_acceso DATE NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES Usuarios(user_id)
);

-- Insertar roles iniciales
INSERT INTO Roles (role_name) VALUES ('Aportador');
INSERT INTO Roles (role_name) VALUES ('Colaborador');

-- Insertar usuarios de prueba
INSERT INTO Usuarios (username, password, role_id) VALUES ('aportador1', 'password1', 1);
INSERT INTO Usuarios (username, password, role_id) VALUES ('colaborador1', 'password1', 2);

-- Insertar residentes de prueba
INSERT INTO Residentes (nombre, fecha_nacimiento, direccion, telefono) 
VALUES ('Juan Perez', TO_DATE('1980-05-15', 'YYYY-MM-DD'), 'Calle Falsa 123', '123456789');

-- Insertar insumos de farmacia de prueba
INSERT INTO Farmacia (nombre_insumo, descripcion, cantidad) 
VALUES ('Paracetamol', 'Analgésico', 100);

-- Insertar registro de recepción de prueba
INSERT INTO Registro_Recepcion (insumo_id, cantidad_recibida, fecha_recepcion, usuario_id) 
VALUES (1, 50, SYSDATE, 1);

-- Insertar registro de acceso de prueba
INSERT INTO Acceso (usuario_id, entidad, entidad_id, fecha_acceso) 
VALUES (1, 'Residente', 1, SYSDATE);
INSERT INTO Acceso (usuario_id, entidad, entidad_id, fecha_acceso) 
VALUES (2, 'Farmacia', 1, SYSDATE);