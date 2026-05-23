CREATE TABLE IF NOT EXISTS puntos_logisticos (
  id INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(160) NOT NULL,
  tipo VARCHAR(40) NOT NULL,
  ciudad VARCHAR(100) NOT NULL,
  estado VARCHAR(100) NOT NULL,
  direccion VARCHAR(255) NOT NULL,
  latitud FLOAT NULL,
  longitud FLOAT NULL,
  activo BOOLEAN NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  PRIMARY KEY (id),
  INDEX ix_puntos_logisticos_id (id),
  INDEX ix_puntos_logisticos_nombre (nombre),
  INDEX ix_puntos_logisticos_tipo (tipo)
);

CREATE TABLE IF NOT EXISTS rutas (
  id INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(120) NOT NULL,
  origen VARCHAR(100) NOT NULL,
  destino VARCHAR(100) NOT NULL,
  origen_id INT NULL,
  destino_id INT NULL,
  distancia_km FLOAT NOT NULL,
  casetas FLOAT NOT NULL,
  trafico INT NOT NULL,
  riesgo INT NOT NULL,
  estado_carretera INT NOT NULL,
  inseguridad INT NOT NULL,
  activa BOOLEAN NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  PRIMARY KEY (id),
  INDEX ix_rutas_id (id),
  INDEX ix_rutas_origen (origen),
  INDEX ix_rutas_destino (destino),
  CONSTRAINT fk_rutas_origen_punto_logistico
    FOREIGN KEY (origen_id) REFERENCES puntos_logisticos (id),
  CONSTRAINT fk_rutas_destino_punto_logistico
    FOREIGN KEY (destino_id) REFERENCES puntos_logisticos (id)
);

CREATE TABLE IF NOT EXISTS transportes (
  id INT NOT NULL AUTO_INCREMENT,
  nombre VARCHAR(120) NOT NULL,
  tipo VARCHAR(30) NOT NULL,
  categoria VARCHAR(30) NULL,
  subcategoria VARCHAR(80) NULL,
  tipo_mercancia VARCHAR(30) NULL,
  refrigerado BOOLEAN NULL,
  combustible VARCHAR(40) NULL,
  costo_km FLOAT NOT NULL,
  velocidad_promedio FLOAT NOT NULL,
  capacidad_kg FLOAT NOT NULL,
  seguridad INT NOT NULL,
  mantenimiento FLOAT NOT NULL,
  costo_operativo FLOAT NOT NULL,
  consumo_por_km FLOAT NOT NULL,
  rendimiento_km_litro FLOAT NULL,
  factor_caseta FLOAT NULL,
  costo_combustible_litro FLOAT NULL,
  descripcion TEXT NULL,
  uso_recomendado TEXT NULL,
  activo BOOLEAN NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  PRIMARY KEY (id),
  INDEX ix_transportes_id (id),
  INDEX ix_transportes_tipo (tipo),
  INDEX ix_transportes_categoria (categoria),
  INDEX ix_transportes_tipo_mercancia (tipo_mercancia)
);

CREATE TABLE IF NOT EXISTS simulaciones (
  id INT NOT NULL AUTO_INCREMENT,
  origen VARCHAR(100) NOT NULL,
  destino VARCHAR(100) NOT NULL,
  peso_kg FLOAT NOT NULL,
  tipo_mercancia VARCHAR(120) NOT NULL,
  prioridad VARCHAR(30) NOT NULL,
  fecha DATE NOT NULL,
  created_at DATETIME NOT NULL,
  PRIMARY KEY (id),
  INDEX ix_simulaciones_id (id),
  INDEX ix_simulaciones_origen (origen),
  INDEX ix_simulaciones_destino (destino)
);

CREATE TABLE IF NOT EXISTS resultados_simulacion (
  id INT NOT NULL AUTO_INCREMENT,
  simulacion_id INT NOT NULL,
  ruta_id INT NOT NULL,
  transporte_id INT NOT NULL,
  costo_total FLOAT NOT NULL,
  tiempo_estimado_horas FLOAT NOT NULL,
  puntaje_riesgo FLOAT NOT NULL,
  consumo_total FLOAT NOT NULL,
  costo_combustible FLOAT NULL,
  casetas_ajustadas FLOAT NULL,
  puntaje_total FLOAT NOT NULL,
  recomendado BOOLEAN NOT NULL,
  created_at DATETIME NOT NULL,
  PRIMARY KEY (id),
  INDEX ix_resultados_simulacion_id (id),
  CONSTRAINT fk_resultados_simulacion_simulacion
    FOREIGN KEY (simulacion_id) REFERENCES simulaciones (id),
  CONSTRAINT fk_resultados_simulacion_ruta
    FOREIGN KEY (ruta_id) REFERENCES rutas (id),
  CONSTRAINT fk_resultados_simulacion_transporte
    FOREIGN KEY (transporte_id) REFERENCES transportes (id)
);
