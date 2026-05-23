import {
  formatCasetas,
  formatCategoria,
  formatCurrency,
  formatMercancia,
  formatNumber,
  formatSubcategoria,
} from "../utils/formatters";

export default function ResultCard({ resultado, simulacion }) {
  if (!resultado) return null;

  const inversa =
    resultado.ruta.origen === simulacion?.destino &&
    resultado.ruta.destino === simulacion?.origen;
  const categoria = resultado.transporte.categoria || resultado.transporte.tipo;
  const labelCasetas = categoria === "terrestre" ? "Casetas ajustadas" : "Casetas";
  const tipoEspecifico = formatSubcategoria(
    resultado.transporte.subcategoria,
    resultado.transporte.nombre
  );

  return (
    <section className="recommended-panel">
      <div className="recommended-copy">
        <span className="badge">Recomendada</span>
        <h2>Top transporte recomendado</h2>
        <div className="recommendation-details">
          <p>
            <span>Ruta recomendada:</span>
            <strong>
              {resultado.ruta.origen} → {resultado.ruta.destino}
            </strong>
          </p>
          <p>
            <span>Transporte recomendado:</span>
            <strong>{resultado.transporte.nombre}</strong>
          </p>
          <p>
            <span>Categoría general:</span>
            <strong>{formatCategoria(categoria)}</strong>
          </p>
          <p>
            <span>Modelo / configuración:</span>
            <strong>{tipoEspecifico}</strong>
          </p>
          <p>
            <span>Tipo de mercancía:</span>
            <strong>{formatMercancia(resultado.transporte.tipo_mercancia || "mixta")}</strong>
          </p>
          <p>
            <span>Refrigeración:</span>
            <strong>{resultado.transporte.refrigerado ? "Refrigerado" : "No refrigerado"}</strong>
          </p>
          <p>
            <span>Uso recomendado:</span>
            <strong>{resultado.transporte.uso_recomendado || "No disponible"}</strong>
          </p>
        </div>
        <p className="recommendation-reason">
          Este transporte fue seleccionado porque obtuvo el mejor puntaje de acuerdo con la
          prioridad elegida.
        </p>
        {inversa && <span className="route-note">Ruta usada en sentido inverso</span>}
      </div>
      <div className="result-metrics">
        <Metric label="Costo total" value={formatCurrency(resultado.costo_total)} />
        <Metric label="Tiempo estimado" value={formatNumber(resultado.tiempo_estimado_horas, " h")} />
        <Metric label="Nivel de riesgo" value={formatNumber(resultado.puntaje_riesgo)} />
        <Metric label="Litros estimados" value={formatNumber(resultado.consumo_total, " L")} />
        <Metric label="Costo de combustible" value={formatCurrency(resultado.costo_combustible)} />
        <Metric label={labelCasetas} value={formatCasetas(resultado.casetas_ajustadas, categoria)} />
        <a
          className="map-button metric-link"
          href={buildRouteMapsUrl(resultado, simulacion)}
          target="_blank"
          rel="noreferrer"
        >
          Ver ruta en Google Maps
        </a>
      </div>
    </section>
  );
}

function Metric({ label, value }) {
  return (
    <span className="metric-card">
      <small>{label}</small>
      <strong>{value}</strong>
    </span>
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
