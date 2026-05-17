import { useEffect, useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import {
  Bar,
  BarChart,
  CartesianGrid,
  Legend,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

import { getSimulacion } from "../api/simulacionesApi";
import DataTable from "../components/DataTable";
import ResultCard from "../components/ResultCard";

export default function ResultadosSimulacion() {
  const { id } = useParams();
  const [simulacion, setSimulacion] = useState(null);
  const [error, setError] = useState("");

  useEffect(() => {
    getSimulacion(id)
      .then((res) => setSimulacion(res.data))
      .catch(() => setError("No se pudieron cargar los resultados."));
  }, [id]);

  const resultados = simulacion?.resultados || [];
  const recomendado = resultados.find((resultado) => resultado.recomendado);

  const chartData = useMemo(
    () =>
      resultados.map((resultado) => ({
        opcion: `${resultado.ruta.nombre} / ${resultado.transporte.nombre}`,
        costo: resultado.costo_total,
        tiempo: resultado.tiempo_estimado_horas,
        riesgo: resultado.puntaje_riesgo,
        consumo: resultado.consumo_total,
      })),
    [resultados]
  );

  const columns = [
    {
      key: "opcion",
      label: "Opción",
      render: (row) => (
        <div>
          <strong>{row.ruta.nombre}</strong>
          <span className="muted-text">{row.transporte.nombre}</span>
          {isRutaInversa(row, simulacion) && (
            <span className="route-note">Ruta usada en sentido inverso</span>
          )}
        </div>
      ),
    },
    { key: "costo_total", label: "Costo", render: (row) => `$${row.costo_total.toLocaleString("es-MX")}` },
    { key: "tiempo_estimado_horas", label: "Horas" },
    {
      key: "puntaje_riesgo",
      label: "Riesgo",
      render: (row) => <span className={riskClass(row.puntaje_riesgo)}>{row.puntaje_riesgo}</span>,
    },
    { key: "consumo_total", label: "Consumo" },
    { key: "puntaje_total", label: "Puntaje" },
    {
      key: "recomendado",
      label: "Resultado",
      render: (row) => (row.recomendado ? <span className="badge">Recomendada</span> : "-"),
    },
  ];

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <p className="eyebrow">Resultados</p>
          <h1>Simulación #{id}</h1>
        </div>
      </div>

      {error && <div className="alert danger">{error}</div>}
      {simulacion && (
        <div className="summary-line">
          {simulacion.origen} a {simulacion.destino} · {simulacion.peso_kg} kg · prioridad{" "}
          {simulacion.prioridad}
        </div>
      )}

      <ResultCard resultado={recomendado} simulacion={simulacion} />

      <section className="section-block">
        <h2>Tabla comparativa</h2>
        <DataTable columns={columns} data={resultados} />
      </section>

      <section className="charts-grid">
        <Chart title="Costo por opción" data={chartData} dataKey="costo" color="#123a63" />
        <Chart title="Tiempo por opción" data={chartData} dataKey="tiempo" color="#1f7a5c" />
        <Chart title="Riesgo por opción" data={chartData} dataKey="riesgo" color="#c2410c" />
        <Chart title="Consumo por opción" data={chartData} dataKey="consumo" color="#9a6b00" />
      </section>
    </div>
  );
}

function Chart({ title, data, dataKey, color }) {
  return (
    <div className="chart-panel">
      <h3>{title}</h3>
      <ResponsiveContainer width="100%" height={260}>
        <BarChart data={data}>
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis dataKey="opcion" hide />
          <YAxis />
          <Tooltip />
          <Legend />
          <Bar dataKey={dataKey} fill={color} radius={[4, 4, 0, 0]} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function riskClass(value) {
  if (value >= 4) return "risk high";
  if (value >= 3) return "risk medium";
  return "risk low";
}

function isRutaInversa(resultado, simulacion) {
  if (!resultado || !simulacion) return false;
  return (
    resultado.ruta.origen === simulacion.destino &&
    resultado.ruta.destino === simulacion.origen
  );
}
