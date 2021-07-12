import copy
from distance_travelled_manager import DistanceTravelledManager
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
    def __init__(self, teams, derbies, restrictions_params, distances,
                 heuristic_params):
        self.teams = teams
        self.derbies = derbies
        self.param_r3 = restrictions_params["r3"]
        self.validator = RestrictionsValidator(teams, derbies,
                                               restrictions_params)
        self.distance_travelled_manager = DistanceTravelledManager(distances)
        self.distances = distances

        # Parametros de la heuristica
        self.n_teams_to_be_swapped = heuristic_params["n_teams_to_be_swapped"]
        self.n_swaps_per_team = heuristic_params["n_swaps_per_team"]
        self.n_iterations = heuristic_params["n_iterations"]

    # Calcula un fixture aleatorio del torneo inicial
    # que cumpla con todas las restricciones
    def calculate_initial_fixture(self):
        print("Calculando fixture. Por favor espere...\n")
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

                    # Actualizo array y diccionario de equipos
                    teams_to_play_per_matchday.remove(local_team)
                    teams_to_play_per_matchday.remove(away_team)
                    teams_to_face_per_team[local_team].remove(away_team)
                    teams_to_face_per_team[away_team].remove(local_team)

                # Fixture incompatible --> Reinicio el fixture
                if dead_end:
                    break

                # Agrego la fecha al fixture
                fixture.append(matchday)

                # Reinicio los equipos por asignar en la fecha
                teams_to_play_per_matchday = copy.deepcopy(self.teams)

            # Fixture compatible --> Salgo del ciclo
            if not dead_end:
                break

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

    '''
    # Recibe el fixture inicial y le aplica la heuristica para
    # minimizar la varianza de los km de viaje de todos los equipos
    def calculate_optimized_fixture(self, fixture):
        print("Optimizando fixture. Por favor espere...")

        # Varianza minima hasta el momento
        min_variance = self.distance_travelled_manager.\
            calculate_km_travelled_variance(fixture)

        # Creo una copia del fixture
        tmp_fixture = copy.deepcopy(fixture)

        # Obtengo la dispersion de los equipos
        teams_dispersion = self.distance_travelled_manager.\
            __calculate_teams_dispersion__(tmp_fixture)

        # Swapeo partidos
        # for matchday in tmp_fixture:
        #     for match in matchday:
        #         # TODO: ...

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
        # Repetir los pasos 1, 2 y 3 tomando la solución previamente obtenida

        return fixture
    '''

    def calculate_optimized_fixture(self, fixture):
        min_variance = float("inf")
        optimized_fixture = None

        for i in range(self.n_iterations):
            print("ITERACIÓN N° " + str(i+1) + "\n")
            tmp_fixture = self.calculate_initial_fixture()
            tmp_variance = self.calculate_km_travelled_variance(tmp_fixture)
            print(str(tmp_variance) + "\n")
            if tmp_variance < min_variance:
                optimized_fixture = tmp_fixture
                min_variance = tmp_variance

        return optimized_fixture

    # Determina si el fixture obtenido es compatible
    def is_compatible(self, fixture):
        return self.validator.validate_fixture(fixture)

    # Devuelve la varianza de los km de viaje de todos los equipos
    def calculate_km_travelled_variance(self, fixture):
        return self.distance_travelled_manager.\
            calculate_km_travelled_variance(fixture)

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
