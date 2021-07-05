import csv
import math
from fixture import Fixture
from restrictions_validator import RestrictionsValidator


def main():
    # Cargo los archivos
    teams = load_teams("csv/test/teams.csv")
    distances = load_distances("csv/test/distances.csv")
    derbies = load_derbies("csv/test/derbies.csv")

    # Creo las clases necesarias
    fixture = Fixture(calculate_fixture(distances, derbies))
    restrictions_validator = RestrictionsValidator()

    # Valido el fixture inicial
    print(restrictions_validator.validate_fixture(fixture.data, derbies, teams))

    # Imprimo el fixture resultante por pantalla
    fixture.print()


# Carga los equipos a partir del archivo csv
def load_teams(path):
    '''
        Formato de los equipos:
        ["Equipo A", ..., "Equipo Z"]
    '''

    teams = []
    with open(path) as f:
        content = f.readlines()
    teams = [x.strip() for x in content]

    return teams


# Carga las distancias a partir del archivo csv
def load_distances(path):
    '''
        Formato de las distancias:
        {"Equipo A": {"Equipo B": 100, ..., "Equipo Z": 200},
        ...,
        "Equipo X": {"Equipo Y": 150, ..., "Equipo Z": 300}
        }
    '''

    distances = {}
    header = True

    with open(path) as csv_file:
        csv_distances = csv.reader(csv_file, delimiter=",")
        for row in csv_distances:
            if header:
                header = False
                continue

            team1, team2, distance = row[0], row[1], row[2]

            if team1 not in distances:
                distances[team1] = {}
            distances[team1][team2] = distance

            if team2 not in distances:
                distances[team2] = {}
            distances[team2][team1] = distance

    return distances


# Carga los derbies a partir del archivo csv
def load_derbies(path):
    '''
    Formato de los derbies:
        {"Equipo A": "Equipo B",
        ...,
        "Equipo Y": "Equipo Z"
        }
    '''

    derbies = {}
    header = True

    with open(path) as csv_file:
        csv_derbies = csv.reader(csv_file, delimiter=",")
        for row in csv_derbies:
            if header:
                header = False
                continue

            team1, team2 = row[0], row[1]

            if team1 not in derbies:
                derbies[team1] = team2

            if team2 not in derbies:
                derbies[team2] = team1

    return derbies


# Calcula el fixture del torneo minimizando la varianza
# de los km de viaje de todos los equipos
def calculate_fixture(distances, derbies):
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
    fixture = [
        [("Boca Juniors", "River Plate"), ("Belgrano", "Talleres")],
        [("Talleres", "Boca Juniors"), ("River Plate", "Belgrano")],
        [("Boca Juniors", "Belgrano"), ("River Plate", "Talleres")]
    ]

    # TODO: cada vez que calculo el fixture, chequear las restricciones.
    # Si no se cumple alguna, tendria que encontrar una forma piola de
    # realizar intercambios hasta que se cumpla o de generar un nuevo fixture
    # de cero que sí cumpla

    return fixture


# Calcula la varianza actual de los km de viaje de todos los equipos
def calculate_km_traveled_variance(fixture, distances):
    km_traveled_variance = 0
    km_traveled_per_team = calculate_km_traveled_per_team(fixture, distances)
    media = calculate_km_traveled_media(km_traveled_per_team)

    for distance in km_traveled_per_team.values():
        km_traveled_variance += (distance - media)**2
    km_traveled_variance/len(km_traveled_per_team)

    return math.sqrt(km_traveled_variance)


# Calcula los km recorridos por cada equipo
def calculate_km_traveled_per_team(fixture, distances):
    '''
    Formato de los km recorridos por equipo:
        {"Equipo A": 100,
        ...,
        "Equipo Z": 200
        }
    '''
    km_traveled_per_team = {}
    for matches in fixture:
        for match in matches:
            local_team, away_team = match[0], match[1]

            if away_team not in km_traveled_per_team:
                km_traveled_per_team[away_team] = 0
            km_traveled_per_team[away_team] +=\
                int(distances[away_team][local_team])

    return km_traveled_per_team


# Calcula la media de los km recorridos por los equipos
def calculate_km_traveled_media(km_traveled_per_team):
    return sum(km_traveled_per_team.values())/len(km_traveled_per_team)


main()
