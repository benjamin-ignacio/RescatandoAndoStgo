from django.db import connection

# SQL para crear la tabla SolicitudVoluntariado
sql = """
CREATE TABLE IF NOT EXISTS mainApp_solicitudvoluntariado (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre_completo VARCHAR(100) NOT NULL,
    email VARCHAR(254) NOT NULL,
    telefono VARCHAR(20) NOT NULL,
    direccion VARCHAR(200) NOT NULL,
    instagram VARCHAR(100) NOT NULL,
    equipo VARCHAR(30) NOT NULL,
    experiencia_previa LONGTEXT NOT NULL,
    motivacion LONGTEXT NOT NULL,
    informacion_adicional LONGTEXT NOT NULL,
    fecha_solicitud DATE NOT NULL,
    estado VARCHAR(30) NOT NULL DEFAULT 'pendiente',
    fecha_entrevista DATETIME NULL,
    link_zoom VARCHAR(200) NOT NULL DEFAULT '',
    observaciones_admin LONGTEXT NOT NULL DEFAULT '',
    procesado_por_id INT NULL,
    FOREIGN KEY (procesado_por_id) REFERENCES mainApp_usuario(id) ON DELETE SET NULL
);
"""

with connection.cursor() as cursor:
    cursor.execute(sql)
    print("✅ Tabla mainApp_solicitudvoluntariado creada exitosamente")
