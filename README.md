# Fixture Para Todos - TP Modelos y Optimización III - FIUBA

## Problema a resolver
Armado del fixture de una liga de fútbol minimizando la varianza de los kilómetros de viaje de todos los equipos

## Consideraciones
- Todos los equipos se enfrentan entre sí una única vez
- El sistema define únicamente los enfrentamientos

## Restricciones
- Todos los equipos deben jugar la misma cantidad de partidos de local y de visitante que el resto o, a lo sumo, un partido de diferencia con respecto al resto de los equipos
- Todos los equipos deben jugar la misma cantidad de partidos de local y de visitante o, a lo sumo, un partido de diferencia entre ambas condiciones
- Ningún equipo puede jugar más de dos partidos consecutivos en la misma condición
- Los equipos considerados clásicos entre sí no pueden jugar de local en la misma fecha

## Relación con Investigación Operativa
- Problema complejo de resolver
- Solución óptima tomaría mucho tiempo
- Solución aproximada con herramientas de IO

## Beneficios Esperados
- Fixture equitativo para todos los equipos
- Equipos con más peso dejan de inclinar la balanza a su favor
- Solución más justa para todos

## Heurística
### Condiciones de corte
- Tiempo máximo de ejecución
- Porcentaje de mejora de la varianza
- Cantidad de iteraciones

### Pasos
#### Paso 1
Armar una solución inicial factible tomando en cada fecha rivales aleatorios, siempre considerando
que los dos equipos no se hayan enfrentado aún y que se cumplan las restricciones mencionadas.
Una vez completa la solución, calcular la varianza de los kilómetros recorridos por todos los equipos.

#### Paso 2
Calcular iterativamente soluciones aleatorias comparándolas con la inicial hasta que se cumpla alguna de las condiciones de corte.

#### Paso 3
Una vez obtenida una nueva solución, se la compara con la solución anterior. Si es mejor, se actualiza; si no, se mantiene la anterior.

#### Paso 4
Devolver la última solución obtenida.