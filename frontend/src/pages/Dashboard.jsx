import { Plus, Trash2 } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getRutas } from "../api/rutasApi";
import { getPuntosLogisticos } from "../api/puntosLogisticosApi";
import { deleteSimulacion, getSimulaciones } from "../api/simulacionesApi";
import { getTransportes } from "../api/transportesApi";
import DataTable from "../components/DataTable";
import StatCard from "../components/StatCard";

export default function Dashboard() {
  const [stats, setStats] = useState({
    puntos: 0,
    rutas: 0,
    transportes: 0,
    simulaciones: 0,
  });
  const [simulaciones, setSimulaciones] = useState([]);
  const [error, setError] = useState("");
  const [message, setMessage] = useState("");

  const loadDashboard = () =>
    Promise.all([getPuntosLogisticos(), getRutas(), getTransportes(), getSimulaciones()])
      .then(([puntosRes, rutasRes, transportesRes, simulacionesRes]) => {
        setStats({
          puntos: puntosRes.data.filter((punto) => punto.activo).length,
          rutas: rutasRes.data.length,
          transportes: transportesRes.data.length,
          simulaciones: simulacionesRes.data.length,
        });
        setSimulaciones(simulacionesRes.data.slice(0, 5));
      });

  useEffect(() => {
    loadDashboard().catch(() => setError("No se pudo conectar con el backend."));
  }, []);

  const removeSimulacion = async (simulacion) => {
    const confirmada = window.confirm(
      `¿Eliminar la simulación #${simulacion.id} y sus resultados guardados?`
    );
    if (!confirmada) return;

    setError("");
    setMessage("");
    try {
      await deleteSimulacion(simulacion.id);
      await loadDashboard();
      setMessage(`Simulación #${simulacion.id} eliminada.`);
    } catch {
      setError("No se pudo eliminar la simulación.");
    }
  };

  const columns = [
    { key: "id", label: "ID" },
    { key: "origen", label: "Origen" },
    { key: "destino", label: "Destino" },
    { key: "peso_kg", label: "Peso kg" },
    { key: "prioridad", label: "Prioridad" },
    {
      key: "acciones",
      label: "Acciones",
      render: (row) => (
        <div className="row-actions">
          <Link className="text-link" to={`/simulaciones/${row.id}`}>Ver</Link>
          <button
            className="icon-button danger"
            type="button"
            onClick={() => removeSimulacion(row)}
            title="Eliminar simulación"
          >
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
          <p className="eyebrow">Panel académico</p>
          <h1>Simulador Logístico Multimodal</h1>
        </div>
        <Link className="primary-button" to="/simulaciones/nueva">
          <Plus size={18} /> Nueva simulación
        </Link>
      </div>

      {error && <div className="alert danger">{error}</div>}
      {message && <div className="alert">{message}</div>}

      <section className="stats-grid">
        <StatCard label="Puntos logísticos" value={stats.puntos} />
        <StatCard label="Rutas generadas" value={stats.rutas} />
        <StatCard label="Transportes activos" value={stats.transportes} tone="green" />
        <StatCard label="Simulaciones" value={stats.simulaciones} tone="orange" />
      </section>

      <section className="section-block">
        <h2>Simulaciones recientes</h2>
        <DataTable columns={columns} data={simulaciones} />
      </section>
    </div>
  );
}
