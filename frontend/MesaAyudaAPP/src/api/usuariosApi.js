import axios from "axios";

const API_URL = "http://127.0.0.1:5000"; // URL de tu backend Flask

export const getUsuarios = async () => {
  try {
    const response = await axios.get(`${API_URL}/usuarios`);
    return response.data;
  } catch (error) {
    console.error("Error al obtener los usuarios:", error);
    throw error;
  }
};
