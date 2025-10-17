import { useEffect, useState } from "react";
import api from "../api/axios";

export default function Tickets() {
  const [tickets, setTickets] = useState([]);

  useEffect(() => {
    api.get("/tickets").then((res) => setTickets(res.data));
  }, []);

  return (
    <div className="p-6">
      <h2 className="text-2xl font-semibold mb-4">Tickets</h2>
      <div className="grid grid-cols-3 gap-4">
        {tickets.map((t) => (
          <div key={t.id_ticket} className="p-4 border rounded shadow">
            <h3 className="font-semibold">Ticket #{t.id_ticket}</h3>
            <p>Estado: {t.estado}</p>
            <p>Prioridad: {t.prioridad}</p>
            <p>Trabajo: {t.id_trabajo}</p>
          </div>
        ))}
      </div>
    </div>
  );
}
