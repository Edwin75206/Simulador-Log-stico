import { Edit, Plus, Trash2, X } from "lucide-react";
import { useEffect, useState } from "react";

import {
  createTransporte,
  deleteTransporte,
  getTransportes,
  updateTransporte,
} from "../api/transportesApi";
import DataTable from "../components/DataTable";

const initialForm = {
  nombre: "",
  tipo: "terrestre",
  costo_km: 1,
  velocidad_promedio: 1,
  capacidad_kg: 1,
  seguridad: 3,
  mantenimiento: 0,
  costo_operativo: 0,
  consumo_por_km: 0,
  activo: true,
};

const numericFields = new Set([
  "costo_km",
  "velocidad_promedio",
  "capacidad_kg",
  "seguridad",
  "mantenimiento",
  "costo_operativo",
  "consumo_por_km",
]);

const securityOptions = [
  { value: 1, label: "1 - Baja seguridad" },
  { value: 2, label: "2 - Seguridad regular" },
  { value: 3, label: "3 - Seguridad media" },
  { value: 4, label: "4 - Seguridad alta" },
  { value: 5, label: "5 - Seguridad muy alta" },
];

export default function Transportes() {
  const [transportes, setTransportes] = useState([]);
  const [form, setForm] = useState(initialForm);
  const [editingId, setEditingId] = useState(null);
  const [message, setMessage] = useState("");

  const loadTransportes = () => getTransportes().then((res) => setTransportes(res.data));

  useEffect(() => {
    loadTransportes().catch(() => setMessage("No se pudieron cargar los transportes."));
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
        await updateTransporte(editingId, form);
      } else {
        await createTransporte(form);
      }
      setForm(initialForm);
      setEditingId(null);
      setMessage("Transporte guardado.");
      await loadTransportes();
    } catch {
      setMessage("Revisa los datos del transporte.");
    }
  };

  const editTransporte = (transporte) => {
    setEditingId(transporte.id);
    setForm({
      nombre: transporte.nombre,
      tipo: transporte.tipo,
      costo_km: transporte.costo_km,
      velocidad_promedio: transporte.velocidad_promedio,
      capacidad_kg: transporte.capacidad_kg,
      seguridad: transporte.seguridad,
      mantenimiento: transporte.mantenimiento,
      costo_operativo: transporte.costo_operativo,
      consumo_por_km: transporte.consumo_por_km,
      activo: transporte.activo,
    });
  };

  const removeTransporte = async (id) => {
    await deleteTransporte(id);
    await loadTransportes();
  };

  const columns = [
    { key: "nombre", label: "Nombre" },
    { key: "tipo", label: "Tipo" },
    { key: "costo_km", label: "Costo/km" },
    { key: "velocidad_promedio", label: "Velocidad" },
    { key: "capacidad_kg", label: "Capacidad kg" },
    { key: "seguridad", label: "Seguridad" },
    { key: "activo", label: "Estado", render: (row) => (row.activo ? "Activo" : "Inactivo") },
    {
      key: "acciones",
      label: "Acciones",
      render: (row) => (
        <div className="row-actions">
          <button className="icon-button" onClick={() => editTransporte(row)} title="Editar">
            <Edit size={16} />
          </button>
          <button className="icon-button danger" onClick={() => removeTransporte(row.id)} title="Eliminar">
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
          <h1>Transportes</h1>
        </div>
      </div>

      {message && <div className="alert">{message}</div>}

      <section className="form-panel">
        <h2>{editingId ? "Editar transporte" : "Agregar transporte"}</h2>
        <form className="grid-form" onSubmit={handleSubmit}>
          <div className="form-section">
            <h3>Datos del transporte</h3>
            <label className="field">
              Nombre del transporte
              <input name="nombre" value={form.nombre} onChange={handleChange} required />
            </label>
            <label className="field">
              Tipo de transporte
              <select name="tipo" value={form.tipo} onChange={handleChange}>
                <option value="terrestre">Terrestre</option>
                <option value="ferroviario">Ferroviario</option>
                <option value="aereo">Aéreo</option>
                <option value="maritimo">Marítimo</option>
              </select>
            </label>
            <label className="field">
              Capacidad máxima en kg
              <input name="capacidad_kg" type="number" min="0.01" step="0.01" value={form.capacidad_kg} onChange={handleChange} required />
            </label>
            <label className="field scale-field">
              Nivel de seguridad
              <select name="seguridad" value={form.seguridad} onChange={handleChange} required>
                {securityOptions.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
              <span className="help-text">
                1 = Baja seguridad, 2 = Seguridad regular, 3 = Seguridad media, 4 = Seguridad alta, 5 = Seguridad muy alta
              </span>
            </label>
            <label className="checkbox-field">
              <input name="activo" type="checkbox" checked={form.activo} onChange={handleChange} />
              Transporte activo
            </label>
          </div>

          <div className="form-section">
            <h3>Costos y rendimiento</h3>
            <label className="field">
              Costo por kilómetro
              <input name="costo_km" type="number" min="0.01" step="0.01" value={form.costo_km} onChange={handleChange} required />
            </label>
            <label className="field">
              Velocidad promedio km/h
              <input name="velocidad_promedio" type="number" min="0.01" step="0.01" value={form.velocidad_promedio} onChange={handleChange} required />
            </label>
            <label className="field">
              Costo de mantenimiento
              <input name="mantenimiento" type="number" min="0" step="0.01" value={form.mantenimiento} onChange={handleChange} required />
            </label>
            <label className="field">
              Costo operativo
              <input name="costo_operativo" type="number" min="0" step="0.01" value={form.costo_operativo} onChange={handleChange} required />
            </label>
            <label className="field">
              Consumo por kilómetro
              <input name="consumo_por_km" type="number" min="0" step="0.01" value={form.consumo_por_km} onChange={handleChange} required />
            </label>
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

      <DataTable columns={columns} data={transportes} />
    </div>
  );
}
