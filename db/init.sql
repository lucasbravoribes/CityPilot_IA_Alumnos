-- Se ejecuta SOLO cuando PostgreSQL inicializa un volumen de datos nuevo.
-- En el taller NO hace falta modificar este archivo.
CREATE TABLE IF NOT EXISTS solicitudes (
  id BIGSERIAL PRIMARY KEY,
  fecha TIMESTAMPTZ NOT NULL DEFAULT NOW(),
  ciudad TEXT NOT NULL,
  pais TEXT,
  tipo_turismo TEXT NOT NULL,
  duracion_horas INTEGER NOT NULL,
  preferencias TEXT NOT NULL DEFAULT '',
  latitud DOUBLE PRECISION,
  longitud DOUBLE PRECISION,
  meteorologia JSONB NOT NULL DEFAULT '{}'::jsonb,
  lugares JSONB NOT NULL DEFAULT '[]'::jsonb,
  prompt_usado TEXT,
  itinerario TEXT,
  modo_demo BOOLEAN NOT NULL DEFAULT FALSE,
  modo_modelo TEXT,
  estado TEXT NOT NULL DEFAULT 'pendiente',
  duracion_ms INTEGER,
  error_resumido TEXT
);
CREATE INDEX IF NOT EXISTS idx_solicitudes_fecha ON solicitudes(fecha DESC);
CREATE INDEX IF NOT EXISTS idx_solicitudes_ciudad ON solicitudes(ciudad);
CREATE INDEX IF NOT EXISTS idx_solicitudes_tipo ON solicitudes(tipo_turismo);
