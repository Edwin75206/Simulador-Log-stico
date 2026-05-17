import { Plus } from "lucide-react";
import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { getRutas } from "../api/rutasApi";
import { getSimulaciones } from "../api/simulacionesApi";
import { getTransportes } from "../api/transportesApi";
import DataTable from "../components/DataTable";
import StatCard from "../components/StatCard";

export default function Dashboard() {
  const [stats, setStats] = useState({ rutas: 0, transportes: 0, simulaciones: 0 });
  const [simulaciones, setSimulaciones] = useState([]);
  const [error, setError] = useState("");

  useEffect(() => {
    Promise.all([getRutas(), getTransportes(), getSimulaciones()])
      .then(([rutasRes, transportesRes, simulacionesRes]) => {
        setStats({
          rutas: rutasRes.data.length,
          transportes: transportesRes.data.length,
          simulaciones: simulacionesRes.data.length,
        });
        setSimulaciones(simulacionesRes.data.slice(0, 5));
      })
      .catch(() => setError("No se pudo conectar con el backend."));
  }, []);

  const columns = [
    { key: "id", label: "ID" },
    { key: "origen", label: "Origen" },
    { key: "destino", label: "Destino" },
    { key: "peso_kg", label: "Peso kg" },
    { key: "prioridad", label: "Prioridad" },
    {
      key: "acciones",
      label: "Resultados",
      render: (row) => <Link className="text-link" to={`/simulaciones/${row.id}`}>Ver</Link>,
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

      <section className="stats-grid">
        <StatCard label="Total de rutas" value={stats.rutas} />
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
