export default function ResultCard({ resultado, simulacion }) {
  if (!resultado) return null;

  const inversa =
    resultado.ruta.origen === simulacion?.destino &&
    resultado.ruta.destino === simulacion?.origen;

  return (
    <section className="recommended-panel">
      <div>
        <span className="badge">Recomendada</span>
        <h2>{resultado.ruta.nombre}</h2>
        <p>
          {resultado.ruta.origen} a {resultado.ruta.destino} con {resultado.transporte.nombre}
        </p>
        {inversa && <span className="route-note">Ruta usada en sentido inverso</span>}
      </div>
      <div className="result-metrics">
        <span>${resultado.costo_total.toLocaleString("es-MX")}</span>
        <span>{resultado.tiempo_estimado_horas} h</span>
        <span>Riesgo {resultado.puntaje_riesgo}</span>
        <span>Consumo {resultado.consumo_total}</span>
      </div>
    </section>
  );
}
