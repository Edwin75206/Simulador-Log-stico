import { Play } from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import { getRutas } from "../api/rutasApi";
import { createSimulacion } from "../api/simulacionesApi";

const today = new Date().toISOString().slice(0, 10);

export default function NuevaSimulacion() {
  const navigate = useNavigate();
  const [form, setForm] = useState({
    origen: "",
    destino: "",
    peso_kg: 1000,
    tipo_mercancia: "Mercancia general",
    prioridad: "equilibrada",
    fecha: today,
  });
  const [rutas, setRutas] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const [loadingRutas, setLoadingRutas] = useState(true);

  useEffect(() => {
    getRutas()
      .then((response) => {
        const rutasActivas = response.data.filter((ruta) => ruta.activa);
        setRutas(rutasActivas);

        const primerOrigen = getLugares(rutasActivas)[0] || "";
        const primerDestino = getDestinosConectados(rutasActivas, primerOrigen)[0] || "";

        setForm((prev) => ({
          ...prev,
          origen: primerOrigen,
          destino: primerDestino,
        }));
      })
      .catch(() => setError("No se pudieron cargar las rutas disponibles."))
      .finally(() => setLoadingRutas(false));
  }, []);

  const origenes = useMemo(
    () => getLugares(rutas),
    [rutas]
  );

  const destinos = useMemo(
    () => getDestinosConectados(rutas, form.origen),
    [rutas, form.origen]
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
    const primerDestino = getDestinosConectados(rutas, nuevoOrigen)[0] || "";

    setForm((prev) => ({
      ...prev,
      origen: nuevoOrigen,
      destino: primerDestino,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    if (!form.origen || !form.destino) {
      setError("Selecciona origen y destino antes de ejecutar la simulación.");
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
      {!loadingRutas && rutas.length === 0 && (
        <div className="alert">
          No hay rutas disponibles. Primero agrega rutas en el catálogo.
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
              disabled={loadingRutas || origenes.length === 0}
              required
            >
              <option value="">
                {loadingRutas ? "Cargando orígenes..." : "Selecciona un origen"}
              </option>
              {origenes.map((origen) => (
                <option key={origen} value={origen}>
                  {origen}
                </option>
              ))}
            </select>
            <span className="help-text">
              Selecciona un origen registrado en el catálogo de rutas.
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
                <option key={destino} value={destino}>
                  {destino}
                </option>
              ))}
            </select>
            <span className="help-text">
              Los destinos disponibles dependen del origen seleccionado.
            </span>
            {form.origen && destinos.length === 0 && (
              <span className="field-warning">No hay destinos disponibles para este origen.</span>
            )}
          </label>
          <label>
            Peso kg
            <input name="peso_kg" type="number" min="0.01" step="0.01" value={form.peso_kg} onChange={handleChange} required />
          </label>
          <label>
            Tipo de mercancía
            <input name="tipo_mercancia" value={form.tipo_mercancia} onChange={handleChange} required />
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
              disabled={loading || !form.origen || !form.destino}
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
  return [...new Set(values.filter(Boolean))];
}

function getLugares(rutas) {
  return getUniqueValues(rutas.flatMap((ruta) => [ruta.origen, ruta.destino]));
}

function getDestinosConectados(rutas, origenSeleccionado) {
  if (!origenSeleccionado) return [];

  return getUniqueValues(
    rutas.flatMap((ruta) => {
      if (ruta.origen === origenSeleccionado) return [ruta.destino];
      if (ruta.destino === origenSeleccionado) return [ruta.origen];
      return [];
    })
  );
}
