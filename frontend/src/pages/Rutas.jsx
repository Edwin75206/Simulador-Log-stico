import { Edit, Plus, Trash2, X } from "lucide-react";
import { useEffect, useState } from "react";

import { createRuta, deleteRuta, getRutas, updateRuta } from "../api/rutasApi";
import DataTable from "../components/DataTable";

const initialForm = {
  nombre: "",
  origen: "",
  destino: "",
  distancia_km: 1,
  casetas: 0,
  trafico: 3,
  riesgo: 3,
  estado_carretera: 3,
  inseguridad: 3,
  activa: true,
};

const numericFields = new Set([
  "distancia_km",
  "casetas",
  "trafico",
  "riesgo",
  "estado_carretera",
  "inseguridad",
]);

const trafficOptions = [
  { value: 1, label: "1 - Muy bajo" },
  { value: 2, label: "2 - Bajo" },
  { value: 3, label: "3 - Medio" },
  { value: 4, label: "4 - Alto" },
  { value: 5, label: "5 - Muy alto" },
];

const roadOptions = [
  { value: 1, label: "1 - Excelente" },
  { value: 2, label: "2 - Bueno" },
  { value: 3, label: "3 - Regular" },
  { value: 4, label: "4 - Malo" },
  { value: 5, label: "5 - Muy malo" },
];

export default function Rutas() {
  const [rutas, setRutas] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
  const [message, setMessage] = useState("");

  const loadRutas = () => getRutas().then((res) => setRutas(res.data));

  useEffect(() => {
    loadRutas().catch(() => setMessage("No se pudieron cargar las rutas."));
  }, []);

  const handleChange = (event) => {
    const { name, value, type, checked } = event.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === "checkbox" ? checked : numericFields.has(name) ? Number(value) : value,
    }));
  };

  const handleSubmit = async (event) => {
    event.preventDefault();
    try {
      if (editingId) {
        await updateRuta(editingId, form);
      } else {
        await createRuta(form);
      }
      setForm(initialForm);
      setEditingId(null);
      setMessage("Ruta guardada.");
      await loadRutas();
    } catch {
      setMessage("Revisa los datos de la ruta.");
    }
  };

  const editRuta = (ruta) => {
    setEditingId(ruta.id);
    setForm({
      nombre: ruta.nombre,
      origen: ruta.origen,
      destino: ruta.destino,
      distancia_km: ruta.distancia_km,
      casetas: ruta.casetas,
      trafico: ruta.trafico,
      riesgo: ruta.riesgo,
      estado_carretera: ruta.estado_carretera,
      inseguridad: ruta.inseguridad,
      activa: ruta.activa,
    });
  };

  const removeRuta = async (id) => {
    await deleteRuta(id);
    await loadRutas();
  };

  const columns = [
    { key: "nombre", label: "Nombre" },
    { key: "origen", label: "Origen" },
    { key: "destino", label: "Destino" },
    { key: "distancia_km", label: "Km" },
    { key: "casetas", label: "Casetas" },
    { key: "trafico", label: "Tráfico" },
    { key: "riesgo", label: "Riesgo" },
    { key: "activa", label: "Estado", render: (row) => (row.activa ? "Activa" : "Inactiva") },
    {
      key: "acciones",
      label: "Acciones",
      render: (row) => (
        <div className="row-actions">
          <button className="icon-button" onClick={() => editRuta(row)} title="Editar">
            <Edit size={16} />
          </button>
          <button className="icon-button danger" onClick={() => removeRuta(row.id)} title="Eliminar">
            <Trash2 size={16} />
          </button>
        </div>
      ),
    },
  ];

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Catálogo</p>
          <h1>Rutas</h1>
        </div>
      </div>

      {message && <div className="alert">{message}</div>}

      <section className="form-panel">
        <h2>{editingId ? "Editar ruta" : "Agregar ruta"}</h2>
        <form className="grid-form" onSubmit={handleSubmit}>
          <div className="form-section">
            <h3>Datos generales</h3>
            <label className="field">
              Nombre de la ruta
              <input name="nombre" value={form.nombre} onChange={handleChange} required />
            </label>
            <label className="field">
              Origen
              <input name="origen" value={form.origen} onChange={handleChange} required />
            </label>
            <label className="field">
              Destino
              <input name="destino" value={form.destino} onChange={handleChange} required />
            </label>
            <label className="field">
              Distancia en kilómetros
              <input name="distancia_km" type="number" min="0.01" step="0.01" value={form.distancia_km} onChange={handleChange} required />
            </label>
            <label className="field">
              Casetas / peajes
              <input name="casetas" type="number" min="0" step="0.01" value={form.casetas} onChange={handleChange} required />
            </label>
            <label className="checkbox-field">
              <input name="activa" type="checkbox" checked={form.activa} onChange={handleChange} />
              Ruta activa
            </label>
          </div>

          <div className="form-section">
            <h3>Evaluación de condiciones</h3>
            <ScaleSelect
              label="Nivel de tráfico"
              name="trafico"
              value={form.trafico}
              onChange={handleChange}
              options={trafficOptions}
              help="1 = Muy bajo, 2 = Bajo, 3 = Medio, 4 = Alto, 5 = Muy alto"
            />
            <ScaleSelect
              label="Nivel de riesgo"
              name="riesgo"
              value={form.riesgo}
              onChange={handleChange}
              options={trafficOptions}
              help="1 = Muy bajo, 2 = Bajo, 3 = Medio, 4 = Alto, 5 = Muy alto"
            />
            <ScaleSelect
              label="Estado de carretera"
              name="estado_carretera"
              value={form.estado_carretera}
              onChange={handleChange}
              options={roadOptions}
              help="1 = Excelente, 2 = Bueno, 3 = Regular, 4 = Malo, 5 = Muy malo"
            />
            <ScaleSelect
              label="Nivel de inseguridad"
              name="inseguridad"
              value={form.inseguridad}
              onChange={handleChange}
              options={trafficOptions}
              help="1 = Muy baja, 2 = Baja, 3 = Media, 4 = Alta, 5 = Muy alta"
            />
          </div>

          <div className="form-actions full">
            <button className="primary-button" type="submit">
              <Plus size={18} /> Guardar
            </button>
            {editingId && (
              <button className="secondary-button" type="button" onClick={() => { setEditingId(null); setForm(initialForm); }}>
                <X size={18} /> Cancelar
              </button>
            )}
          </div>
        </form>
      </section>

      <DataTable columns={columns} data={rutas} />
    </div>
  );
}

function ScaleSelect({ label, name, value, onChange, options, help }) {
  return (
    <label className="field scale-field">
      {label}
      <select name={name} value={value} onChange={onChange} required>
        {options.map((option) => (
          <option key={option.value} value={option.value}>
            {option.label}
          </option>
        ))}
      </select>
      <span className="help-text">{help}</span>
    </label>
  );
}
