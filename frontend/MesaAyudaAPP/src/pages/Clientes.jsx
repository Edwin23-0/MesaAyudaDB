import React, { useEffect, useState } from "react";
import { getUsuarios } from "../api/usuariosApi";

const Clientes = () => {
  const [usuarios, setUsuarios] = useState([]);

  useEffect(() => {
    const fetchUsuarios = async () => {
      try {
        const data = await getUsuarios();
        setUsuarios(data);
      } catch (error) {
        console.error("Error cargando usuarios:", error);
      }
    };

    fetchUsuarios();
  }, []);

  return (
    <div className="p-6 bg-gray-50 min-h-screen">
      <h1 className="text-3xl font-bold mb-6 text-blue-700">Lista de Usuarios</h1>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {usuarios.map((usuario) => (
          <div
            key={usuario.id_usuario}
            className="p-4 bg-white rounded-xl shadow-md hover:shadow-lg transition-all"
          >
            <h2 className="text-xl font-semibold text-gray-800 mb-2">
              {usuario.nombre}
            </h2>
            <p><strong>Email:</strong> {usuario.email}</p>
            <p><strong>Teléfono:</strong> {usuario.telefono}</p>
            <p><strong>Rol:</strong> {usuario.rol}</p>
            <p><strong>Especialidad:</strong> {usuario.especialidad}</p>
          </div>
        ))}
      </div>
    </div>
  );
};

export default Clientes;
