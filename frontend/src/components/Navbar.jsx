import { BarChart3, Map, PackageSearch, Route, Truck } from "lucide-react";
import { NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <aside className="sidebar">
      <div className="brand">
        <PackageSearch size={28} />
        <div>
          <strong>Simulador</strong>
          <span>Logística multimodal</span>
        </div>
      </div>
      <nav className="nav-links">
        <NavLink to="/">
          <BarChart3 size={18} /> Dashboard
        </NavLink>
        <NavLink to="/rutas">
          <Route size={18} /> Rutas
        </NavLink>
        <NavLink to="/transportes">
          <Truck size={18} /> Transportes
        </NavLink>
        <NavLink to="/simulaciones/nueva">
          <Map size={18} /> Nueva simulación
        </NavLink>
      </nav>
    </aside>
  );
}
