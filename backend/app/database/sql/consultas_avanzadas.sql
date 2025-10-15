
-- 1️⃣ Técnicos con mayor cantidad de tickets cerrados
SELECT 
    u.nombre AS Tecnico,
    COUNT(t.id_ticket) AS Total_Cerrados
FROM dbo.Ticket t
INNER JOIN dbo.Trabajo tr ON t.id_trabajo = tr.id_trabajo
INNER JOIN dbo.UsuarioSistema u ON tr.id_tecnico = u.id_usuario
WHERE t.estado = 'Cerrado'
GROUP BY u.nombre
ORDER BY Total_Cerrados DESC;

-- 2️⃣ Promedio de tiempo de resolución de tickets por técnico
SELECT 
    u.nombre AS Tecnico,
    AVG(DATEDIFF(HOUR, t.fecha_creacion, t.fecha_cierre)) AS Promedio_Horas_Resolucion
FROM dbo.Ticket t
INNER JOIN dbo.Trabajo tr ON t.id_trabajo = tr.id_trabajo
INNER JOIN dbo.UsuarioSistema u ON tr.id_tecnico = u.id_usuario
WHERE t.estado = 'Cerrado'
GROUP BY u.nombre
ORDER BY Promedio_Horas_Resolucion ASC;

-- 3️⃣ Clientes con más tickets creados
SELECT 
    c.nombre AS Cliente,
    COUNT(t.id_ticket) AS Total_Tickets
FROM dbo.Ticket t
INNER JOIN dbo.ServicioCliente sc ON t.id_servicio_cliente = sc.id_servicio_cliente
INNER JOIN dbo.Cliente c ON sc.id_cliente = c.id_cliente
GROUP BY c.nombre
ORDER BY Total_Tickets DESC;

-- 4️⃣ Tipos de problema más comunes
SELECT 
    tp.descripcion AS Tipo_Problema,
    COUNT(t.id_ticket) AS Total_Incidencias
FROM dbo.Ticket t
INNER JOIN dbo.TipoProblema tp ON t.id_tipo_problema = tp.id_tipo_problema
GROUP BY tp.descripcion
ORDER BY Total_Incidencias DESC;

-- 5️⃣ Porcentaje de tickets cerrados frente al total
SELECT 
    (COUNT(CASE WHEN estado = 'Cerrado' THEN 1 END) * 100.0 / COUNT(*)) AS Porcentaje_Cerrados
FROM dbo.Ticket;

-- 6️⃣ Equipos más reportados en tickets
SELECT 
    e.nombre_equipo,
    COUNT(dt.id_detalle) AS Total_Reportes
FROM dbo.DetalleTrabajo dt
INNER JOIN dbo.Equipoinstalado e ON dt.id_equipo = e.id_equipo
GROUP BY e.nombre_equipo
ORDER BY Total_Reportes DESC;

-- 7️⃣ Técnicos que atienden más de 5 tickets abiertos actualmente
SELECT 
    u.nombre AS Tecnico,
    COUNT(t.id_ticket) AS Tickets_Abiertos
FROM dbo.Ticket t
INNER JOIN dbo.Trabajo tr ON t.id_trabajo = tr.id_trabajo
INNER JOIN dbo.UsuarioSistema u ON tr.id_tecnico = u.id_usuario
WHERE t.estado = 'Abierto'
GROUP BY u.nombre
HAVING COUNT(t.id_ticket) > 5;

-- 8️⃣ Tiempo promedio de resolución por tipo de problema
SELECT 
    tp.descripcion AS Tipo_Problema,
    AVG(DATEDIFF(HOUR, t.fecha_creacion, t.fecha_cierre)) AS Promedio_Horas
FROM dbo.Ticket t
INNER JOIN dbo.TipoProblema tp ON t.id_tipo_problema = tp.id_tipo_problema
WHERE t.estado = 'Cerrado'
GROUP BY tp.descripcion
ORDER BY Promedio_Horas ASC;

-- 9️⃣ Días con más creación de tickets
SELECT 
    CONVERT(DATE, t.fecha_creacion) AS Fecha,
    COUNT(*) AS Total_Tickets
FROM dbo.Ticket t
GROUP BY CONVERT(DATE, t.fecha_creacion)
ORDER BY Total_Tickets DESC;

-- 🔟 Técnicos con mejor rendimiento (cerrados / asignados)
SELECT 
    u.nombre AS Tecnico,
    COUNT(CASE WHEN t.estado = 'Cerrado' THEN 1 END) * 100.0 / COUNT(*) AS Eficiencia_Porcentaje
FROM dbo.Ticket t
INNER JOIN dbo.Trabajo tr ON t.id_trabajo = tr.id_trabajo
INNER JOIN dbo.UsuarioSistema u ON tr.id_tecnico = u.id_usuario
GROUP BY u.nombre
ORDER BY Eficiencia_Porcentaje DESC;
