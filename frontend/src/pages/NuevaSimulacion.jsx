import { Play } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { getPuntosLogisticos } from "../api/puntosLogisticosApi";
import { createSimulacion } from "../api/simulacionesApi";

const today = new Date().toISOString().slice(0, 10);

export default function NuevaSimulacion() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    origen: "",
    destino: "",
    peso_kg: 1000,
    tipo_mercancia: "mixta",
    prioridad: "equilibrada",
    fecha: today,
  });
  const [puntos, setPuntos] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingPuntos, setLoadingPuntos] = useState(true);

  useEffect(() => {
    getPuntosLogisticos()
      .then((response) => {
        const puntosActivos = response.data.filter((punto) => punto.activo);
        setPuntos(puntosActivos);

        const opciones = getOpcionesPuntos(puntosActivos);
        const primerOrigen = opciones[0]?.value || "";
        const primerDestino = opciones.find((punto) => punto.value !== primerOrigen)?.value || "";

        setForm((prev) => ({
          ...prev,
          origen: primerOrigen,
          destino: primerDestino,
        }));
      })
      .catch(() => setError("No se pudieron cargar los puntos logísticos disponibles."))
      .finally(() => setLoadingPuntos(false));
  }, []);

  const origenes = useMemo(
    () => getOpcionesPuntos(puntos),
    [puntos]
  );

  const destinos = useMemo(
    () => origenes.filter((punto) => punto.value !== form.origen),
    [origenes, form.origen]
  );

  const handleChange = (event) => {
    const { name, value, type } = event.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === "number" ? Number(value) : value,
    }));
  };

  const handleOrigenChange = (event) => {
    const nuevoOrigen = event.target.value;
    const destinoActualDisponible = destinos.some((destino) => destino.value === form.destino);
    const primerDestino = origenes.find((punto) => punto.value !== nuevoOrigen)?.value || "";

    setForm((prev) => ({
      ...prev,
      origen: nuevoOrigen,
      destino:
        destinoActualDisponible && prev.destino !== nuevoOrigen
          ? prev.destino
          : primerDestino,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!form.origen || !form.destino || form.origen === form.destino) {
      setError("Selecciona dos puntos logísticos distintos antes de ejecutar la simulación.");
      return;
    }

    setLoading(true);
    setError("");
    try {
      const response = await createSimulacion(form);
      navigate(`/simulaciones/${response.data.id}`);
    } catch (err) {
      setError(err.response?.data?.detail || "No se pudo ejecutar la simulación.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page narrow">
      <div className="page-header">
        <div>
          <p className="eyebrow">Comparación multimodal</p>
          <h1>Nueva simulación</h1>
        </div>
      </div>

      {error && <div className="alert danger">{error}</div>}
      {!loadingPuntos && puntos.length === 0 && (
        <div className="alert">
          No hay puntos logísticos disponibles. Primero agrega puntos al catálogo.
        </div>
      )}

      <section className="form-panel">
        <form className="grid-form two" onSubmit={handleSubmit}>
          <label className="field">
            Origen
            <select
              name="origen"
              value={form.origen}
              onChange={handleOrigenChange}
              disabled={loadingPuntos || origenes.length === 0}
              required
            >
              <option value="">
                {loadingPuntos ? "Cargando orígenes..." : "Selecciona un origen"}
              </option>
              {origenes.map((origen) => (
                <option key={origen.value} value={origen.value}>
                  {origen.label}
                </option>
              ))}
            </select>
            <span className="help-text">
              Puedes seleccionar cualquier punto logístico registrado como origen.
            </span>
          </label>
          <label className="field">
            Destino
            <select
              name="destino"
              value={form.destino}
              onChange={handleChange}
              disabled={!form.origen || destinos.length === 0}
              required
            >
              <option value="">
                {form.origen && destinos.length === 0
                  ? "Sin destinos disponibles"
                  : "Selecciona un destino"}
              </option>
              {destinos.map((destino) => (
                <option key={destino.value} value={destino.value}>
                  {destino.label}
                </option>
              ))}
            </select>
            <span className="help-text">
              Elige cualquier otro punto logístico; no puede ser igual al origen.
            </span>
            {form.origen && destinos.length === 0 && (
              <span className="field-warning">No hay destinos disponibles para este origen.</span>
            )}
          </label>
          <p className="help-text full">
            Puedes seleccionar cualquier punto logístico registrado como origen y cualquier otro
            como destino. El sistema generará o usará una ruta simulada entre ambos.
          </p>
          <label>
            Peso kg
            <input name="peso_kg" type="number" min="0.01" step="0.01" value={form.peso_kg} onChange={handleChange} required />
          </label>
          <label>
            Tipo de mercancía
            <select name="tipo_mercancia" value={form.tipo_mercancia} onChange={handleChange} required>
              <option value="mixta">Mixta</option>
              <option value="perecedera">Perecedera</option>
              <option value="no_perecedera">No perecedera</option>
            </select>
          </label>
          <label>
            Prioridad
            <select name="prioridad" value={form.prioridad} onChange={handleChange}>
              <option value="equilibrada">Equilibrada</option>
              <option value="costo">Costo</option>
              <option value="tiempo">Tiempo</option>
              <option value="seguridad">Seguridad</option>
              <option value="recursos">Recursos</option>
            </select>
          </label>
          <label>
            Fecha
            <input name="fecha" type="date" value={form.fecha} onChange={handleChange} required />
          </label>
          <div className="form-actions full">
            <button
              className="primary-button"
              type="submit"
              disabled={loading || !form.origen || !form.destino || form.origen === form.destino}
            >
              <Play size={18} /> {loading ? "Calculando..." : "Ejecutar simulación"}
            </button>
          </div>
        </form>
      </section>
    </div>
  );
}

function getUniqueValues(values) {
  const seen = new Set();
  return values.filter((item) => {
    if (!item?.value || seen.has(item.value)) return false;
    seen.add(item.value);
    return true;
  });
}

function getOpcionesPuntos(puntos) {
  return getUniqueValues(
    puntos.map((punto) => ({
      value: punto.nombre,
      label: `${punto.nombre} - ${punto.ciudad}, ${punto.estado}`,
    }))
  );
}
