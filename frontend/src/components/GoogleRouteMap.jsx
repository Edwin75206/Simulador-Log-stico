export default function GoogleRouteMap({ origin, destination, externalUrl, height = 360 }) {
  const apiKey = import.meta.env.VITE_GOOGLE_MAPS_EMBED_API_KEY;
  const hasRoute = Boolean(origin && destination);

  if (!apiKey || !hasRoute) {
    return (
      <div className="map-placeholder" style={{ minHeight: height }}>
        <p>
          Para mostrar el mapa embebido, configura VITE_GOOGLE_MAPS_EMBED_API_KEY en
          frontend/.env.
        </p>
        {externalUrl && (
          <div className="map-actions">
            <a className="map-button" href={externalUrl} target="_blank" rel="noreferrer">
              Abrir ruta en Google Maps
            </a>
          </div>
        )}
      </div>
    );
  }

  const src =
    "https://www.google.com/maps/embed/v1/directions" +
    `?key=${encodeURIComponent(apiKey)}` +
    `&origin=${encodeURIComponent(origin)}` +
    `&destination=${encodeURIComponent(destination)}` +
    "&mode=driving";

  return (
    <iframe
      className="google-map-frame"
      title="Ruta en Google Maps"
      src={src}
      height={height}
      loading="lazy"
      referrerPolicy="no-referrer-when-downgrade"
      allowFullScreen
    />
  );
}
