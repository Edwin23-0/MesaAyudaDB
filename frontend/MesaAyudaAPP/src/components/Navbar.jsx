import { Link } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="bg-blue-600 text-white px-8 py-4 flex justify-between items-center shadow-md">
      <h1 className="text-2xl font-bold">Mesa de Ayuda</h1>
      <ul className="flex gap-6">
        <li><Link to="/" className="hover:text-gray-200">Dashboard</Link></li>
        <li><Link to="/clientes" className="hover:text-gray-200">Clientes</Link></li>
        <li><Link to="/tickets" className="hover:text-gray-200">Tickets</Link></li>
        <li><Link to="/trabajos" className="hover:text-gray-200">Trabajos</Link></li>
        <li><Link to="/catalogo" className="hover:text-gray-200">Catálogo</Link></li>
      </ul>
    </nav>
  );
}
