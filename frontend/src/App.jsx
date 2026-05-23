import { Navigate, Route, Routes } from "react-router-dom";

import Navbar from "./components/Navbar";
import Dashboard from "./pages/Dashboard";
import NuevaSimulacion from "./pages/NuevaSimulacion";
import PuntosLogisticos from "./pages/PuntosLogisticos";
import ResultadosSimulacion from "./pages/ResultadosSimulacion";
import Rutas from "./pages/Rutas";
import Transportes from "./pages/Transportes";

export default function App() {
  return (
    <div className="app-shell">
      <Navbar />
      <main className="main-content">
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/puntos-logisticos" element={<PuntosLogisticos />} />
          <Route path="/rutas" element={<Rutas />} />
          <Route path="/transportes" element={<Transportes />} />
          <Route path="/simulaciones/nueva" element={<NuevaSimulacion />} />
          <Route path="/simulaciones/:id" element={<ResultadosSimulacion />} />
          <Route path="*" element={<Navigate to="/" replace />} />
        </Routes>
      </main>
    </div>
  );
}
