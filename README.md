# Fixture Para Todos - TP Modelos y Optimización - FIUBA

## Problema a resolver
Armado del fixture de una liga de fútbol minimizando la varianza de los kilómetros de viaje de todos los equipos

## Consideraciones
- Todos los equipos se enfrentan entre sí una única vez
- El sistema define únicamente los enfrentamientos

## Restricciones
- Todos los equipos deben jugar la misma cantidad de partidos de local y de visitante que el resto
- Todos los equipos deben jugar la misma cantidad de partidos de local y de visitante o, a lo sumo, un partido de diferencia entre ambas condiciones
- Ningún equipo puede jugar más de tres veces dos partidos consecutivos en la misma condición
- Los equipos considerados clásicos entre sí no pueden jugar en la misma condición en la misma fecha

## Relación con Investigación Operativa
- Problema complejo de resolver
- Solución óptima tomaría mucho tiempo
- Solución aproximada con herramientas de IO

## Beneficios Esperados
- Fixture equitativo para todos los equipos
- Equipos con más peso dejan de inclinar la balanza a su favor
- Solución más justa para todos

## Heurística
### Paso 1
Armar una solución inicial factible tomando siempre en cada fecha el rival más cercano, siempre considerando
que los dos equipos no se hayan enfrentado aún y que se cumplan las restricciones mencionadas.
Una vez completa la solución, calcular la varianza de los kilómetros recorridos por todos los equipos.

### Paso 2

### Paso 3

### Paso 4