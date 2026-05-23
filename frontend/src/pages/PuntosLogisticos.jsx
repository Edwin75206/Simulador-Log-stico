import { ExternalLink } from "lucide-react";
import { useEffect, useMemo, useState } from "react";

import { getPuntosLogisticos } from "../api/puntosLogisticosApi";
import DataTable from "../components/DataTable";

const tipos = {
  central_abasto: "Central de abasto",
  puerto: "Puerto",
  central_autobuses: "Central de autobuses",
  aeropuerto: "Aeropuerto",
};

export default function PuntosLogisticos() {
  const [puntos, setPuntos] = useState([]);
  const [tipo, setTipo] = useState("todos");
  const [message, setMessage] = useState("");

  useEffect(() => {
    getPuntosLogisticos()
      .then((response) => setPuntos(response.data.filter((punto) => punto.activo)))
      .catch(() => setMessage("No se pudieron cargar los puntos logísticos."));
  }, []);

  const puntosFiltrados = useMemo(() => {
    if (tipo === "todos") return puntos;
    return puntos.filter((punto) => punto.tipo === tipo);
  }, [puntos, tipo]);

  const columns = [
    { key: "nombre", label: "Nombre" },
    { key: "tipo", label: "Tipo", render: (row) => tipos[row.tipo] || row.tipo },
    { key: "ciudad", label: "Ciudad" },
    { key: "estado", label: "Estado" },
    {
      key: "maps",
      label: "Google Maps",
      render: (row) => (
        <a className="map-button" href={row.google_maps_url} target="_blank" rel="noreferrer">
          <ExternalLink size={15} /> Ver
        </a>
      ),
    },
  ];

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Catálogo logístico</p>
          <h1>Puntos logísticos</h1>
        </div>
      </div>

      {message && <div className="alert danger">{message}</div>}

      <section className="form-panel compact-panel">
        <label className="field filter-field">
          Filtrar por tipo
          <select value={tipo} onChange={(event) => setTipo(event.target.value)}>
            <option value="todos">Todos</option>
            <option value="central_abasto">Centrales de abasto</option>
            <option value="puerto">Puertos</option>
            <option value="central_autobuses">Centrales de autobuses</option>
            <option value="aeropuerto">Aeropuertos</option>
          </select>
        </label>
      </section>

      <DataTable columns={columns} data={puntosFiltrados} />
    </div>
  );
}
