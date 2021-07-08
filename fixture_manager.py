import copy
import random
from restrictions_validator import RestrictionsValidator


class FixtureManager(object):
    '''
    Formato del fixture (cada elemento de la lista es una fecha):
        [
            [("Equipo A", "Equipo B"),
            (..., ...),
            ("Equipo Y", "Equipo Z")],
            ...,
            [("Equipo A", "Equipo B"),
            (..., ...),
            ("Equipo Y", "Equipo Z")]
        ]
    '''
    def __init__(self, teams, derbies, restrictions_params, distances):
        self.teams = teams
        self.derbies = derbies
        self.param_r3 = restrictions_params["r3"]
        self.validator = RestrictionsValidator(teams, derbies,
                                               restrictions_params)
        self.distances = distances

    # Calcula un fixture aleatorio del torneo inicial
    # que cumpla con todas las restricciones
    def calculate_initial_fixture(self):
        print("Calculando fixture inicial. Por favor espere...")
        while True:
            fixture = self.__calculate_initial_fixture__()
            if self.is_compatible(fixture):
                break

        return fixture

    def __calculate_initial_fixture__(self):
        # Cantidad de fechas
        n_matchdays = len(self.teams) - 1

        # Cantidad de partidos por fecha
        n_matches = int(len(self.teams) / 2)

        # Iteracion hasta encontrar un fixture compatible
        while True:
            # Fixture
            fixture = []

            # Array para saber que equipos quedan por asignar en la fecha
            teams_to_play_per_matchday = copy.deepcopy(self.teams)

            # Diccionario para saber a que equipos resta enfrentar cada equipo
            teams_to_face_per_team = {i: [] for i in self.teams}
            for team in teams_to_face_per_team:
                teams_to_face_per_team[team] = copy.deepcopy(self.teams)
                teams_to_face_per_team[team].remove(team)

            # Boolean para saber si entre en un dead-end
            dead_end = False

            for _ in range(n_matchdays):
                matchday = []
                for _ in range(n_matches):
                    # Equipo local
                    local_team = self.__calculate_local_team__(
                        fixture, matchday, teams_to_play_per_matchday)

                    # Si no hay ninguno factible, salgo del ciclo
                    # y reinicio el fixture
                    if not local_team:
                        dead_end = True
                        break

                    # Equipo visitante
                    away_team = self.__calculate_away_team__(
                        fixture, teams_to_play_per_matchday,
                        teams_to_face_per_team, local_team)

                    # Si no hay ninguno factible, salgo del ciclo
                    # y reinicio el fixture
                    if not away_team:
                        dead_end = True
                        break

                    # Agrego el partido a la fecha
                    matchday.append((local_team, away_team))

                    # DEBUG
                    # print("FECHA " + str(x+1))
                    # print("\n")
                    # print("Equipos por asignar en la fecha:")
                    # print(teams_to_play_per_matchday)
                    # print("\n")
                    # print("Equipos a enfrentar por cada equipo:")
                    # print(teams_to_face_per_team)
                    # print("\n")
                    # print("Partido:")
                    # print(local_team + " Vs. " + away_team)
                    # print("\n")

                    # Actualizo array y diccionario de equipos
                    teams_to_play_per_matchday.remove(local_team)
                    teams_to_play_per_matchday.remove(away_team)
                    teams_to_face_per_team[local_team].remove(away_team)
                    teams_to_face_per_team[away_team].remove(local_team)

                # Si entre en un dead-end salgo del ciclo
                # y reinicio el fixture
                if dead_end:
                    break

                # Agrego la fecha al fixture
                fixture.append(matchday)

                # Reinicio los equipos por asignar en la fecha
                teams_to_play_per_matchday = copy.deepcopy(self.teams)

            # Fixture compatible --> Salgo del ciclo
            if not dead_end:
                break

        # Chequeo que se cumplan las restricciones
        # TODO: deberia chequear R1 y R2
        # Idea: si no se cumplen, meter todo en un while
        # hasta que devuelva True el validator

        return fixture

    # Obtiene un equipo local aleatorio que cumpla las restricciones
    # y que no haya jugado la fecha actual
    def __calculate_local_team__(self, fixture, matchday,
                                 teams_to_play_per_matchday):
        # Equipos cuyo clasico no sea local en esta misma fecha
        teams_ok_1 = copy.deepcopy(teams_to_play_per_matchday)
        for match in matchday:
            local_team = match[0]
            derby_team = self.derbies[local_team]
            if derby_team not in teams_to_play_per_matchday:
                continue
            teams_ok_1.remove(derby_team)

        # Equipos que no hayan jugado los ultimos <param_r3> partidos de local
        teams_ok_2 = copy.deepcopy(teams_to_play_per_matchday)
        last_played_per_team = {i: 0 for i in teams_to_play_per_matchday}
        for matchday in fixture[-self.param_r3:]:
            for match in matchday:
                local_team = match[0]
                if local_team not in teams_to_play_per_matchday:
                    continue
                last_played_per_team[local_team] += 1
                if last_played_per_team[local_team] == self.param_r3:
                    teams_ok_2.remove(local_team)

        # Interseccion de los arrays obtenidos
        available_teams = list(set(teams_ok_1) & set(teams_ok_2))

        if len(available_teams) == 0:
            return None

        return random.choice(available_teams)

    # Obtiene un equipo visitante aleatorio que cumpla las restricciones,
    # que no haya jugado la fecha actual y que no se haya enfrentado
    # al equipo local actual
    def __calculate_away_team__(self, fixture, teams_to_play_per_matchday,
                                teams_to_face_per_team, local_team):
        # Equipos que aun no se hayan enfrentado al equipo local
        teams_ok_1 = copy.deepcopy(teams_to_face_per_team[local_team])

        # Equipos que no hayan jugado los ultimos <param_r3>
        # partidos de visitante
        teams_ok_2 = copy.deepcopy(teams_to_play_per_matchday)
        last_played_per_team = {i: 0 for i in teams_to_play_per_matchday}
        for matchday in fixture[-self.param_r3:]:
            for match in matchday:
                away_team = match[1]
                if away_team not in teams_to_play_per_matchday:
                    continue
                last_played_per_team[away_team] += 1
                if last_played_per_team[away_team] == self.param_r3:
                    teams_ok_2.remove(away_team)

        # Interseccion de los arrays obtenidos
        available_teams = list(set(teams_ok_1) & set(teams_ok_2))

        if len(available_teams) == 0:
            return None

        return random.choice(available_teams)

    # Recibe el fixture inicial y le aplica la heuristica para
    # minimizar la varianza de los km de viaje de todos los equipos
    def calculate_optimized_fixture(self, fixture):
        print("Optimizando fixture inicial. Por favor espere...")
        # TODO: codear esta funcion teniendo en cuenta la varianza

        # Paso 1
        # Seleccionar los N equipos con mayor dispersión de la media
        # (es decir, aquellos que más impacto negativo tienen en la varianza)
        # y alternar su condición en los M partidos que tienen mayor
        # distancia recorrida, para así acercarse a la media.

        # Paso 2
        # En cada intercambio se debe comprobar que las restricciones
        # se sigan cumpliendo para todos los equipos. Si alguna restricción
        # no se cumple, se selecciona el siguiente intercambio candidato.

        # Paso 3
        # Una vez obtenida la solución, se la compara con la solución anterior.
        # Si es mejor, se actualiza; si no, se mantiene la anterior.

        # Paso 4
        # Repetir los pasos 1, 2 y 3 tomando la última solución obtenida,
        # evitando repetir intercambios previamente realizados,
        # al menos por J iteraciones (para así explorar nuevas soluciones).

        return fixture

    # Determina si el fixture obtenido es compatible
    def is_compatible(self, fixture):
        return self.validator.validate_fixture(fixture)

    # Imprime el fixture por pantalla
    def print(self, fixture):
        print("--------------------------------------------------------------")
        print("--------------------- FIXTURE PARA TODOS ---------------------")
        print("--------------------------------------------------------------")

        i = 1
        for matchday in fixture:
            print("\nFecha " + str(i) + ":")
            i += 1

            for match in matchday:
                local_team, away_team = match[0], match[1]
                local_tabs = "\t\t" if len(local_team) >= 8 else "\t\t\t"
                away_tabs = "\t\t"
                print("\t" + local_team + local_tabs + "Vs." +
                      away_tabs + away_team)
