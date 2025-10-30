-- ¿Cuántos alumnos tienen suspenso al menos un proyecto EN MADRID Y VALENCIA?
SELECT
bootcamp.vertical,
campus.ciudad,
calificacion.resultado,
COUNT (DISTINCT alumno.alumnoid)


FROM alumno
INNER JOIN bootcamp ON bootcamp.bootcampid = alumno.bootcampid
INNER JOIN calificacion ON alumno.alumnoid = calificacion.alumnoid
INNER JOIN proyecto ON calificacion.proyectoid = proyecto.proyectoid
INNER JOIN aula ON bootcamp.aulaid = aula.aulaid
INNER JOIN campus ON aula.campusid = campus.campusid

WHERE calificacion.resultado = 'No Apto'
GROUP BY 1,2,3;


-- ¿Qué aulas han sido usadas en los distintos bootcamps impartidos hasta ahora?
SELECT
DISTINCT aula.nombre,
campus.ciudad,
bootcamp.vertical,
modalidad.tipo,
modalidad.dedicacion,
promocion.fecha_inicio,
promocion.fecha_fin


FROM bootcamp
INNER JOIN alumno ON bootcamp.bootcampid = alumno.bootcampid
INNER JOIN calificacion ON alumno.alumnoid = calificacion.alumnoid
INNER JOIN proyecto ON calificacion.proyectoid = proyecto.proyectoid
INNER JOIN aula ON bootcamp.aulaid = aula.aulaid
INNER JOIN campus ON aula.campusid = campus.campusid
INNER JOIN profe_curso ON profe_curso.bootcampid = bootcamp.bootcampid
INNER JOIN profesor ON profe_curso.profesorid = profesor.profesorid
INNER JOIN modalidad ON bootcamp.modalidadid = modalidad.modalidadid
INNER JOIN promocion ON bootcamp.promocionid = promocion.promocionid

-- ¿Qué profesores han impartido el bootcamp en madrid?
SELECT
profesor.nombre ||' '|| profesor.apellido AS nombre,
profesor.rol,
campus.ciudad, 
promocion.nombre,
promocion.fecha_inicio,
promocion.fecha_fin


FROM bootcamp

INNER JOIN profe_curso ON profe_curso.bootcampid = bootcamp.bootcampid
INNER JOIN profesor ON profe_curso.profesorid = profesor.profesorid
INNER JOIN campus ON campus.campusid = profesor.campusid
INNER JOIN promocion ON bootcamp.promocionid = promocion.promocionid

WHERE campus.ciudad = 'Madrid'


