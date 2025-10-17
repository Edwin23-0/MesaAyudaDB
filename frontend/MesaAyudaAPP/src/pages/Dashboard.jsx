import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Dashboard() {
  const [resumen, setResumen] = useState({});

  useEffect(() => {
    api.get("/dashboard/resumen").then((res) => setResumen(res.data));
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-semibold mb-4">Panel General</h2>
      <div className="grid grid-cols-3 gap-4">
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-gray-600">Clientes</h3>
          <p className="text-2xl font-bold">{resumen.clientes}</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-gray-600">Tickets Activos</h3>
          <p className="text-2xl font-bold">{resumen.tickets_activos}</p>
        </div>
        <div className="bg-white p-4 rounded-lg shadow">
          <h3 className="text-gray-600">Trabajos Pendientes</h3>
          <p className="text-2xl font-bold">{resumen.trabajos_pendientes}</p>
        </div>
      </div>
    </div>
  );
}
