
-- 1️⃣ Promedio de días por técnico (ya la tienes)
SELECT 
    u.nombre AS Tecnico,
    COUNT(t.id_trabajo) AS Total_Trabajos,
    AVG(DATEDIFF(DAY, t.fecha_creacion, GETDATE())) AS Promedio_Dias_Trabajo
FROM dbo.Trabajo t
JOIN dbo.UsuarioSistema u ON t.id_tecnico = u.id_usuario
WHERE u.rol = 'tecnico'
GROUP BY u.nombre
ORDER BY Promedio_Dias_Trabajo ASC;

-- 2️⃣ Técnicos con más de 5 trabajos asignados (usa HAVING)
SELECT 
    u.nombre AS Tecnico,
    COUNT(t.id_trabajo) AS Total_Trabajos
FROM dbo.Trabajo t
JOIN dbo.UsuarioSistema u ON t.id_tecnico = u.id_usuario
WHERE u.rol = 'tecnico'
GROUP BY u.nombre
HAVING COUNT(t.id_trabajo) > 5
ORDER BY Total_Trabajos DESC;

-- 3️⃣ Clientes con más de un tipo de servicio activo
SELECT 
    c.nombre AS Cliente,
    COUNT(DISTINCT s.id_tipo) AS Tipos_Servicio_Activos
FROM dbo.ServicioCliente s
JOIN dbo.Cliente c ON s.id_cliente = c.id_cliente
WHERE s.estado = 'activo'
GROUP BY c.nombre
HAVING COUNT(DISTINCT s.id_tipo) > 1;

-- 4️⃣ Promedio de validaciones por supervisor (usa AVG + GROUP BY)
SELECT 
    u.nombre AS Supervisor,
    COUNT(v.id_validacion) AS Total_Validaciones,
    AVG(CASE WHEN v.resultado = 1 THEN 1 ELSE 0 END) * 100 AS Porcentaje_Aprobadas
FROM dbo.Validacion v
JOIN dbo.UsuarioSistema u ON v.id_supervisor = u.id_usuario
WHERE u.rol = 'supervisor'
GROUP BY u.nombre
ORDER BY Porcentaje_Aprobadas DESC;

-- 5️⃣ Top 5 clientes con más tickets creados (usa TOP + ORDER BY)
SELECT TOP 5 
    c.nombre AS Cliente,
    COUNT(tk.id_ticket) AS Total_Tickets
FROM dbo.Ticket tk
JOIN dbo.Trabajo tr ON tk.id_trabajo = tr.id_trabajo
JOIN dbo.Cliente c ON tr.id_cliente = c.id_cliente
GROUP BY c.nombre
ORDER BY Total_Tickets DESC;


-- 6️⃣ Tickets que cambiaron más veces de estado (usa COUNT + HistorialTicket)
SELECT 
    tk.id_ticket,
    COUNT(h.id_historial) AS Total_Cambios_Estado
FROM dbo.HistorialTicket h
JOIN dbo.Ticket tk ON h.id_ticket = tk.id_ticket
GROUP BY tk.id_ticket
HAVING COUNT(h.id_historial) > 3
ORDER BY Total_Cambios_Estado DESC;


-- 7️⃣ Tiempo promedio entre creación y validación de tickets (usa subconsulta + AVG)
SELECT 
    AVG(DATEDIFF(DAY, tk.fecha_creado, v.fecha_validacion)) AS Promedio_Dias_Validacion
FROM dbo.Ticket tk
JOIN dbo.Validacion v ON tk.id_ticket = v.id_ticket;


-- 8️⃣ Catálogos más usados en tickets (usa GROUP BY + COUNT)
SELECT 
    c.nombre AS Catalogo,
    COUNT(tk.id_ticket) AS Veces_Usado
FROM dbo.Ticket tk
JOIN dbo.Catalogo c ON tk.id_catalogo = c.id_catalogo
GROUP BY c.nombre
ORDER BY Veces_Usado DESC;

-- 9️⃣ Técnicos que más validaciones exitosas tienen (usa subconsulta y ORDER BY)
SELECT 
    u.nombre AS Supervisor,
    (SELECT COUNT(*) 
     FROM dbo.Validacion v 
     WHERE v.id_supervisor = u.id_usuario AND v.resultado = 1) AS Validaciones_Exitosas
FROM dbo.UsuarioSistema u
WHERE u.rol = 'supervisor'
ORDER BY Validaciones_Exitosas DESC;


-- 🔟 Ranking de técnicos por eficiencia (usa CTE y función de ventana)
WITH Eficiencia AS (
    SELECT 
        u.id_usuario,
        u.nombre AS Tecnico,
        COUNT(t.id_trabajo) AS Total_Trabajos,
        AVG(DATEDIFF(DAY, t.fecha_creacion, GETDATE())) AS Promedio_Dias
    FROM dbo.Trabajo t
    JOIN dbo.UsuarioSistema u ON t.id_tecnico = u.id_usuario
    WHERE u.rol = 'tecnico'
    GROUP BY u.id_usuario, u.nombre
)
SELECT 
    Tecnico,
    Total_Trabajos,
    Promedio_Dias,
    RANK() OVER (ORDER BY Total_Trabajos DESC, Promedio_Dias ASC) AS Ranking_Eficiencia
FROM Eficiencia;
