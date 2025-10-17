import React from "react";
import "../styles/home.css";

const Home = () => {
  return (
    <div className="home-container">
      <header className="home-header">
        <h1 className="home-title">Mesa de Ayuda</h1>
        <p className="home-subtitle">Gestión eficiente de tickets y soporte técnico</p>
      </header>

      <section className="home-content">
        <div className="home-card">
          <h2>Atiende tus tickets</h2>
          <p>Administra, asigna y da seguimiento a las solicitudes de los usuarios de manera rápida y organizada.</p>
          <button className="home-btn">Ir a Tickets</button>
        </div>

        <div className="home-card">
          <h2>Gestión de clientes</h2>
          <p>Visualiza y gestiona la información de tus clientes para ofrecer un mejor servicio técnico.</p>
          <button className="home-btn">Ver Clientes</button>
        </div>

        <div className="home-card">
          <h2>Panel de control</h2>
          <p>Obtén una vista general de las métricas más importantes de tu sistema de soporte.</p>
          <button className="home-btn">Ir al Dashboard</button>
        </div>
      </section>
    </div>
  );
};

export default Home;
