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
import GoogleRouteMap from "../components/GoogleRouteMap";
import ResultCard from "../components/ResultCard";
import {
  formatCasetas,
  formatCategoria,
  formatCurrency,
  formatMercancia,
  formatNumber,
  formatSubcategoria,
} from "../utils/formatters";

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
  const recommendedMapsUrl = buildRouteMapsUrl(recomendado, simulacion);
  const recommendedMapPoints = buildEmbedMapPoints(recomendado, simulacion);

  const chartData = useMemo(
    () =>
      resultados.map((resultado) => ({
        opcion: resultado.transporte.nombre,
        ruta: resultado.ruta.nombre,
        rutaTexto: `${resultado.ruta.origen} → ${resultado.ruta.destino}`,
        transporte: resultado.transporte.nombre,
        transporteCorto: truncateLabel(resultado.transporte.nombre, 34),
        categoria: formatCategoria(resultado.transporte.categoria || resultado.transporte.tipo),
        tipoEspecifico: formatSubcategoria(
          resultado.transporte.subcategoria,
          resultado.transporte.nombre
        ),
        costo: resultado.costo_total,
        tiempo: resultado.tiempo_estimado_horas,
        riesgo: resultado.puntaje_riesgo,
        consumo: resultado.consumo_total,
      })),
    [resultados]
  );

  const columns = [
    {
      key: "ruta",
      label: "Ruta",
      render: (row) => (
        <div>
          <strong>{row.ruta.nombre}</strong>
          {isRutaInversa(row, simulacion) && (
            <span className="route-note">Ruta usada en sentido inverso</span>
          )}
        </div>
      ),
    },
    { key: "transporte", label: "Transporte", render: (row) => row.transporte.nombre },
    {
      key: "categoria",
      label: "Categoría general",
      render: (row) => formatCategoria(row.transporte.categoria || row.transporte.tipo),
    },
    {
      key: "tipo_especifico",
      label: "Modelo / configuración",
      render: (row) => formatSubcategoria(row.transporte.subcategoria, row.transporte.nombre),
    },
    { key: "costo_total", label: "Costo total", render: (row) => formatCurrency(row.costo_total) },
    {
      key: "velocidad_promedio",
      label: "Velocidad promedio",
      render: (row) => formatNumber(row.transporte.velocidad_promedio, " km/h"),
    },
    { key: "tiempo_estimado_horas", label: "Tiempo", render: (row) => formatNumber(row.tiempo_estimado_horas, " h") },
    {
      key: "puntaje_riesgo",
      label: "Riesgo",
      render: (row) => <span className={riskClass(row.puntaje_riesgo)}>{formatNumber(row.puntaje_riesgo)}</span>,
    },
    { key: "consumo_total", label: "Litros", render: (row) => formatNumber(row.consumo_total, " L") },
    {
      key: "costo_combustible",
      label: "Combustible",
      render: (row) => formatCurrency(row.costo_combustible),
    },
    {
      key: "casetas_ajustadas",
      label: "Casetas",
      render: (row) =>
        formatCasetas(row.casetas_ajustadas, row.transporte.categoria || row.transporte.tipo),
    },
    {
      key: "mercancia",
      label: "Mercancía",
      render: (row) => formatMercancia(row.transporte.tipo_mercancia || "mixta"),
    },
    {
      key: "refrigerado",
      label: "Refrigerado",
      render: (row) => (row.transporte.refrigerado ? "Sí" : "No"),
    },
    { key: "puntaje_total", label: "Puntaje" },
    {
      key: "recomendado",
      label: "Resultado",
      render: (row) => (row.recomendado ? <span className="badge">Recomendada</span> : "-"),
    },
    {
      key: "maps",
      label: "Google Maps",
      render: (row) => (
        <a
          className="map-button"
          href={buildRouteMapsUrl(row, simulacion)}
          target="_blank"
          rel="noreferrer"
        >
          Ver ruta
        </a>
      ),
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
        <section className="simulation-summary">
          <h2>Resumen de simulación</h2>
          <div className="summary-grid">
            <SummaryItem label="Origen" value={simulacion.origen} />
            <SummaryItem label="Destino" value={simulacion.destino} />
            <SummaryItem label="Peso" value={`${simulacion.peso_kg.toLocaleString("es-MX")} kg`} />
            <SummaryItem label="Mercancía" value={formatMercancia(simulacion.tipo_mercancia)} />
            <SummaryItem label="Prioridad" value={formatMercancia(simulacion.prioridad)} />
          </div>
        </section>
      )}

      <ResultCard resultado={recomendado} simulacion={simulacion} />

      {recomendado && (
        <section className="map-card">
          <div className="map-card-header">
            <div>
              <h2>Vista de ruta en Google Maps</h2>
              <p>Mapa referencial generado con Google Maps.</p>
            </div>
            <div className="map-actions">
              <a
                className="map-button"
                href={recommendedMapsUrl}
                target="_blank"
                rel="noreferrer"
              >
                Abrir ruta en Google Maps
              </a>
            </div>
          </div>
          <GoogleRouteMap
            origin={recommendedMapPoints.origin}
            destination={recommendedMapPoints.destination}
            externalUrl={recommendedMapsUrl}
          />
        </section>
      )}

      <section className="section-block">
        <h2>Tabla comparativa</h2>
        <p className="section-description">
          La siguiente tabla compara las alternativas disponibles de transporte para la ruta
          seleccionada. La opción recomendada se determina a partir del costo, tiempo, riesgo y
          consumo, según la prioridad elegida.
        </p>
        <DataTable columns={columns} data={resultados} />
      </section>

      <section className="charts-grid">
        <Chart
          title="Costo total por transporte"
          subtitle="Compara el costo estimado de cada alternativa logística."
          data={chartData}
          dataKey="costo"
          yLabel="Costo MXN"
          valueLabel="Costo total"
          formatter={formatCurrency}
          color="#123a63"
        />
        <Chart
          title="Tiempo estimado por transporte"
          subtitle="Muestra cuántas horas tarda cada alternativa."
          data={chartData}
          dataKey="tiempo"
          yLabel="Horas"
          valueLabel="Tiempo estimado"
          formatter={(value) => formatNumber(value, " h")}
          color="#1f7a5c"
        />
        <Chart
          title="Nivel de riesgo por transporte"
          subtitle="Mientras menor sea el valor, más segura es la alternativa."
          data={chartData}
          dataKey="riesgo"
          yLabel="Puntaje de riesgo"
          valueLabel="Riesgo"
          formatter={formatNumber}
          color="#c2410c"
        />
        <Chart
          title="Litros estimados por transporte"
          subtitle="Compara el consumo estimado de combustible."
          data={chartData}
          dataKey="consumo"
          yLabel="Litros"
          valueLabel="Litros estimados"
          formatter={(value) => formatNumber(value, " L")}
          color="#9a6b00"
        />
      </section>
    </div>
  );
}

function Chart({ title, subtitle, data, dataKey, color, yLabel, valueLabel, formatter }) {
  const chartHeight = Math.max(420, data.length * 34 + 120);

  return (
    <div className="chart-panel chart-card-large">
      <div className="chart-heading">
        <h3>{title}</h3>
        <p className="chart-subtitle">{subtitle}</p>
      </div>
      <ResponsiveContainer width="100%" height={chartHeight}>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 8, right: 32, left: 120, bottom: 28 }}
        >
          <CartesianGrid strokeDasharray="3 3" />
          <XAxis
            type="number"
            label={{ value: yLabel, position: "insideBottom", offset: -12 }}
            tick={{ fontSize: 12 }}
          />
          <YAxis
            type="category"
            dataKey="transporteCorto"
            width={190}
            tick={{ fontSize: 12 }}
          />
          <Tooltip content={<ChartTooltip dataKey={dataKey} valueLabel={valueLabel} formatter={formatter} />} />
          <Legend />
          <Bar dataKey={dataKey} fill={color} radius={[0, 4, 4, 0]} name={valueLabel} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

function ChartTooltip({ active, payload, dataKey, valueLabel, formatter }) {
  if (!active || !payload?.length) return null;
  const item = payload[0].payload;
  return (
    <div className="chart-tooltip">
      <span>Ruta: {item.rutaTexto}</span>
      <strong>Transporte: {item.transporte}</strong>
      <span>Categoría: {item.categoria}</span>
      <span>Tipo específico: {item.tipoEspecifico}</span>
      <span>
        {valueLabel}: {formatter ? formatter(item[dataKey]) : item[dataKey]}
      </span>
    </div>
  );
}

function truncateLabel(value, maxLength) {
  if (!value || value.length <= maxLength) return value;
  return `${value.slice(0, maxLength - 1)}…`;
}

function SummaryItem({ label, value }) {
  return (
    <div className="summary-item">
      <span>{label}</span>
      <strong>{value}</strong>
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

function buildRouteMapsUrl(resultado, simulacion) {
  if (!resultado || !simulacion) return resultado?.ruta?.google_maps_url || "#";

  const origen =
    resultado.ruta.origen === simulacion.origen
      ? mapsValue(resultado.ruta.punto_origen, resultado.ruta.origen)
      : mapsValue(resultado.ruta.punto_destino, resultado.ruta.destino);
  const destino =
    resultado.ruta.destino === simulacion.destino
      ? mapsValue(resultado.ruta.punto_destino, resultado.ruta.destino)
      : mapsValue(resultado.ruta.punto_origen, resultado.ruta.origen);

  return `https://www.google.com/maps/dir/?api=1&origin=${encodeURIComponent(
    origen
  )}&destination=${encodeURIComponent(destino)}&travelmode=driving`;
}

function mapsValue(punto, fallback) {
  if (punto?.latitud != null && punto?.longitud != null) {
    return `${punto.latitud},${punto.longitud}`;
  }
  if (punto) return `${punto.nombre} ${punto.ciudad} ${punto.estado}`;
  return fallback;
}

function buildEmbedMapPoints(resultado, simulacion) {
  if (!resultado || !simulacion) {
    return {
      origin: simulacion?.origen || "",
      destination: simulacion?.destino || "",
    };
  }

  const origin =
    resultado.ruta.origen === simulacion.origen
      ? mapsValue(resultado.ruta.punto_origen, resultado.ruta.origen)
      : mapsValue(resultado.ruta.punto_destino, resultado.ruta.destino);
  const destination =
    resultado.ruta.destino === simulacion.destino
      ? mapsValue(resultado.ruta.punto_destino, resultado.ruta.destino)
      : mapsValue(resultado.ruta.punto_origen, resultado.ruta.origen);

  return {
    origin: origin || simulacion.origen,
    destination: destination || simulacion.destino,
  };
}
