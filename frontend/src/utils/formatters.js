export function formatCategoria(value) {
  const categorias = {
    terrestre: "Terrestre",
    aereo: "Aéreo",
    maritimo: "Marítimo",
    ferroviario: "Ferroviario",
  };
  return categorias[value] || formatTitle(value || "No disponible");
}

export function formatSubcategoria(value, fallback = "No disponible") {
  const subcategorias = {
    camioneta_carga: "Camioneta de carga",
    camioneta_refrigerada: "Camioneta refrigerada",
    camion_rabon: "Camión rabón",
    camion_rabon_refrigerado: "Camión rabón refrigerado",
    torton: "Torton",
    torton_refrigerado: "Torton refrigerado",
    trailer_sencillo: "Tráiler caja seca 53 pies",
    trailer_refrigerado: "Tráiler refrigerado 53 pies",
    full_trailer: "Full tráiler doble remolque caja seca",
    full_trailer_refrigerado: "Full tráiler doble remolque refrigerado",
    avion_ligero_carga: "Avión ligero carguero Cessna 208B",
    avion_regional_carga: "Avión regional carguero ATR 72",
    turbohelice_carguero: "Avión turbohélice carguero ATR 42",
    boeing_737_carguero: "Boeing 737 carguero",
    boeing_757_carguero: "Boeing 757 carguero",
    boeing_767_carguero: "Boeing 767 carguero",
    airbus_a330_carguero: "Airbus A330 carguero",
    boeing_777_carguero: "Boeing 777 carguero",
    boeing_747_carguero: "Boeing 747 carguero",
    antonov_carga_sobredimensionada: "Antonov carga sobredimensionada",
    lancha_carga_costera: "Lancha de carga costera",
    barcaza_carga: "Barcaza de carga",
    buque_feeder: "Buque feeder",
    buque_portacontenedores_pequeno: "Buque portacontenedores pequeño",
    buque_portacontenedores_mediano: "Buque portacontenedores mediano",
    buque_portacontenedores_grande: "Buque portacontenedores grande",
    buque_refrigerado: "Buque refrigerado",
    buque_granelero: "Buque granelero",
    buque_ro_ro: "Buque Ro-Ro",
    buque_tanque: "Buque tanque",
    tren_carga_general: "Tren de carga general",
    tren_carga_general_ge_es44ac: "Tren de carga general GE ES44AC",
    tren_intermodal_doble_estiba: "Tren intermodal doble estiba",
    tren_refrigerado_multimodal: "Tren refrigerado multimodal",
    tren_granelero_tolvas: "Tren granelero de tolvas",
    tren_automotriz_madrina: "Tren automotriz madrina ferroviaria",
  };
  if (!value) return fallback;
  return subcategorias[value] || formatTitle(value);
}

export function formatMercancia(value) {
  const tipos = {
    mixta: "Mixta",
    perecedera: "Perecedera",
    no_perecedera: "No perecedera",
  };
  return tipos[value] || formatTitle(value || "No disponible");
}

export function formatCurrency(value) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "No disponible";
  }
  return `$${Number(value).toLocaleString("es-MX")}`;
}

export function formatNumber(value, suffix = "") {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return "No disponible";
  }
  return `${Number(value).toLocaleString("es-MX")}${suffix}`;
}

export function formatCasetas(value, categoria) {
  if (value === null || value === undefined || Number.isNaN(Number(value))) {
    return categoria === "terrestre" ? "No disponible" : "No aplica";
  }
  if (Number(value) === 0 && categoria === "terrestre") return "No disponible";
  if (Number(value) === 0 && categoria !== "terrestre") return "No aplica";
  return `$${Number(value).toLocaleString("es-MX")}`;
}

export function formatTitle(value) {
  return String(value)
    .replace(/_/g, " ")
    .split(" ")
    .filter(Boolean)
    .map((word, index) => {
      if (index > 0 && ["de", "del", "la", "el"].includes(word.toLowerCase())) {
        return word.toLowerCase();
      }
      return word.charAt(0).toUpperCase() + word.slice(1);
    })
    .join(" ");
}
