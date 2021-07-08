import copy
import random


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
    def __init__(self, teams, distances):
        self.teams = teams
        self.distances = distances

    # Calcula el fixture del torneo minimizando la varianza
    # de los km de viaje de todos los equipos
    def calculate_initial_fixture(self):
        '''
        fixture = [
            [("Boca Juniors", "River Plate"), ("Belgrano", "Talleres")],
            [("Talleres", "Boca Juniors"), ("River Plate", "Belgrano")],
            [("Boca Juniors", "Belgrano"), ("Talleres", "River Plate")]
        ]
        '''

        # TODO: cada vez que calculo el fixture, chequear las restricciones.
        # Si no se cumple alguna, tendria que encontrar una forma piola de
        # realizar intercambios hasta que se cumpla o de generar
        # un nuevo fixture de cero que sí cumpla

        # Cantidad de fechas
        n_matchdays = len(self.teams) - 1

        # Cantidad de partidos por fecha
        n_matches = int(len(self.teams) / 2)

        # Fixture
        fixture = []

        # Array para saber que equipos quedan por asignar en la fecha actual
        teams_to_play_per_matchday = copy.deepcopy(self.teams)

        # Diccionario para saber a que equipos resta enfrentar cada equipo
        teams_to_face_per_team = {i: [] for i in self.teams}
        for team in teams_to_face_per_team:
            teams_to_face_per_team[team] = copy.deepcopy(self.teams)
            teams_to_face_per_team[team].remove(team)

        # Iteracion inicial
        for x in range(n_matchdays):
            matchday = []
            for y in range(n_matches):
                # Equipo local
                local_team = self.__calculate_local_team__(
                    fixture, matchday, teams_to_play_per_matchday)

                # Equipo visitante
                away_team = self.__calculate_away_team__(
                    fixture, teams_to_play_per_matchday,
                    teams_to_face_per_team, local_team)

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

                # Limpio array y diccionario de equipos
                teams_to_play_per_matchday.remove(local_team)
                teams_to_play_per_matchday.remove(away_team)
                teams_to_face_per_team[local_team].remove(away_team)
                teams_to_face_per_team[away_team].remove(local_team)

            # Agrego la fecha al fixture
            fixture.append(matchday)

            # Reinicio los equipos por asignar en la fecha
            teams_to_play_per_matchday = copy.deepcopy(self.teams)

        # Chequeo que se cumplan las restricciones
        # TODO: deberia chequear R1 y R2
        # Idea: si no se cumplen, meter todo en un while
        # hasta que devuelva True el validator

        return fixture

    # Obtiene un equipo local aleatorio que cumpla las restricciones
    # y que no haya jugado la fecha actual
    def __calculate_local_team__(self, fixture, matchday,
                                 teams_to_play_per_matchday):
        # TODO: el local team debe cumplir:
        # - Que no haya jugado los ultimos dos de local (ver fixture)
        # - Que su clasico no sea local en esta misma fecha (ver matchday)
        # - Que no haya jugado la fecha actual
        return random.choice(teams_to_play_per_matchday)

    # Obtiene un equipo visitante aleatorio que cumpla las restricciones,
    # que no haya jugado la fecha actual y que no se haya enfrentado
    # al equipo local actual
    def __calculate_away_team__(self, fixture, teams_to_play_per_matchday,
                                teams_to_face_per_team, local_team):
        # TODO: el away team debe cumplir:
        # - Que no haya jugado los ultimos dos de visitante (ver fixture)
        # - Que no haya jugado la fecha actual
        # - Que no se haya enfrentado aun al local team
        available_teams = list(set(teams_to_play_per_matchday) &
                               set(teams_to_face_per_team[local_team]))

        return random.choice(available_teams)

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
                print("\t" + local_team + "\t\tVs.\t\t" + away_team)
